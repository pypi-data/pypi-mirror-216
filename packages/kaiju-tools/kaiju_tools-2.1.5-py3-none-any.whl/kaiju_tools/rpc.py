"""RPC services and classes."""

import abc
import asyncio
import os
import warnings
from binascii import b2a_hex
from enum import Enum
from fnmatch import fnmatch
from time import time
from typing import cast, List, Union, TypedDict, Callable, Dict, Optional, Tuple, Awaitable, NewType, Any

from kaiju_tools.interfaces import (
    AbstractRPCCompatible,
    SessionInterface,
    PublicInterface,
    RPCServer,
    RPCClient,
    AuthenticationInterface,
)
from kaiju_tools.annotations import AnnotationParser, FunctionAnnotation
from kaiju_tools.functions import get_short_uid, timeout, retry
from kaiju_tools.jsonschema import compile_schema
from kaiju_tools.templates import Template
from kaiju_tools.app import Service, ContextableService, Scheduler
from kaiju_tools.serialization import Serializable
from kaiju_tools.encoding import MsgpackType, msgpack_types, ReservedClassIDs, msgpack_dumps, msgpack_loads
from kaiju_tools.app import REQUEST_CONTEXT, REQUEST_SESSION, RequestContext
from kaiju_tools.sessions import TokenClientService
from kaiju_tools.types import Scope, Session
from kaiju_tools.exceptions import *

__all__ = (
    'JSONRPC',
    'RPCMessage',
    'RPCRequest',
    'RPCResponse',
    'RPCError',
    'JSONRPCHeaders',
    'AbstractRPCCompatible',
    'PermissionKeys',
    'AbstractTokenInterface',
    'RPCClientError',
    'RPCServer',
    'RPCClient',
    'RequestHeaders',
    'MethodInfo',
    'JSONRPCServer',
    'Scope',
    'Session',
    'BaseRPCClient',
)

JSONRPC = '2.0'  #: protocol version


class RPCMessage(Serializable, MsgpackType, abc.ABC):
    """Base JSONRPC message class."""


class RPCRequest(RPCMessage):
    """Valid JSONRPC request."""

    ext_class_id = ReservedClassIDs.jsonrpc_request

    __slots__ = ('id', 'method', 'params')

    def __init__(self, id: Union[int, None], method: str = None, params: Union[list, dict] = None):
        """Initialize."""
        self.id = id
        self.method = method
        self.params = params if params else None

    def repr(self):
        """Create a JSONRPC body."""
        data = {'jsonrpc': JSONRPC, 'id': self.id, 'method': self.method, 'params': self.params}
        return data

    def to_bytes(self) -> bytes:
        """Dump to msgpack."""
        return msgpack_dumps((self.id, self.method, self.params))

    @classmethod
    def from_bytes(cls, data: bytes) -> dict:
        """Load from msgpack."""
        data = msgpack_loads(data)
        return {'jsonrpc': JSONRPC, 'id': data[0], 'method': data[1], 'params': data[2]}


class RPCResponse(RPCMessage):
    """Valid JSON RPC response."""

    ext_class_id = ReservedClassIDs.jsonrpc_response

    __slots__ = ('id', 'result')

    def __init__(self, id: Union[int, None], result: Any):
        """Initialize."""
        self.id = id
        self.result = result

    def repr(self):
        """Create a JSONRPC body."""
        return {'jsonrpc': JSONRPC, 'id': self.id, 'result': self.result}

    def to_bytes(self) -> bytes:
        """Dump to msgpack."""
        return msgpack_dumps((self.id, self.result))

    @classmethod
    def from_bytes(cls, data: bytes) -> dict:
        """Load from msgpack."""
        data = msgpack_loads(data)
        return {'jsonrpc': JSONRPC, 'id': data[0], 'result': data[1]}


class RPCError(RPCMessage):
    """RPC error object."""

    ext_class_id = ReservedClassIDs.jsonrpc_error

    __slots__ = ('id', 'error')

    def __init__(self, id: Union[int, None], error: APIException):
        """Initialize."""
        self.id = id
        self.error = error

    def repr(self) -> dict:
        """Create a JSONRPC body."""
        return {'jsonrpc': JSONRPC, 'id': self.id, 'error': self.error.repr()}

    def to_bytes(self) -> bytes:
        """Dump to msgpack."""
        return msgpack_dumps((self.id, self.error))

    @classmethod
    def from_bytes(cls, data: bytes) -> dict:
        """Load from msgpack."""
        data = msgpack_loads(data)
        return {'jsonrpc': JSONRPC, 'id': data[0], 'error': data[1]}


msgpack_types.register_class(RPCRequest)
msgpack_types.register_class(RPCResponse)
msgpack_types.register_class(RPCError)


class JSONRPCHeaders:
    """List of JSONRPC request / response headers."""

    AUTHORIZATION = 'Authorization'
    CONTENT_TYPE_HEADER = 'Content-Type'
    USER_AGENT = 'User-Agent'

    APP_ID_HEADER = 'App-Id'
    SERVER_ID_HEADER = 'Server-Id'
    CORRELATION_ID_HEADER = 'Correlation-Id'

    REQUEST_DEADLINE_HEADER = 'Deadline'
    REQUEST_TIMEOUT_HEADER = 'Timeout'
    RETRIES = 'RPC-Retries'
    CALLBACK_ID = 'RPC-Callback'
    ABORT_ON_ERROR = 'RPC-Batch-Abort-Error'
    USE_TEMPLATE = 'RPC-Batch-Template'

    SESSION_ID_HEADER = 'Session-Id'


class PermissionKeys:
    """Permission scopes."""

    GLOBAL_SYSTEM_PERMISSION = Scope.SYSTEM
    GLOBAL_USER_PERMISSION = Scope.USER
    GLOBAL_GUEST_PERMISSION = Scope.GUEST


class AbstractTokenInterface(abc.ABC):
    """Describes a token provider service methods to be able to be used by the :class:`.AbstractRPCClientService`."""

    @abc.abstractmethod
    async def get_token(self) -> str:
        """Must always return a valid auth token."""


class RPCClientError(APIException):
    """JSON RPC Python exception class."""

    def __init__(self, *args, response=None, **kws):
        super().__init__(*args, **kws)
        self.response = response

    def __str__(self):
        return self.message


_RequestId = NewType('_RequestId', Union[int, None])


class _Task(asyncio.Task):
    deadline: int
    started: int


class _Aborted(APIException):
    pass


class RequestHeaders(TypedDict):
    """Request headers acknowledged by the server."""

    correlation_id: str
    request_deadline: int
    abort_on_error: bool
    use_template: bool
    retries: int


class MethodInfo(TypedDict):
    """Stored method data."""

    f: Callable
    signature: FunctionAnnotation
    service_name: str
    permission: Scope
    validator: Callable


class JSONRPCServer(ContextableService, PublicInterface, RPCServer):
    """A simple JSON RPC interface with method execution and management tasks."""

    service_name = 'rpc'
    _permission_levels = {
        PublicInterface.PermissionKeys.GLOBAL_SYSTEM_PERMISSION: Scope.SYSTEM,
        PublicInterface.PermissionKeys.GLOBAL_USER_PERMISSION: Scope.USER,
        PublicInterface.PermissionKeys.GLOBAL_GUEST_PERMISSION: Scope.GUEST,
    }

    def __init__(
        self,
        app,
        *,
        session_service: SessionInterface = None,
        auth_service: AuthenticationInterface = None,
        max_parallel_tasks: int = 64,
        default_request_time: int = 120,
        max_request_time: int = 600,
        enable_permissions: bool = True,
        request_logs: bool = False,
        response_logs: bool = False,
        blacklist_routes: List[str] = None,
        blacklist_scope: int = Scope.SYSTEM.value - 1,
        use_annotation_parser: bool = True,
        logger=None,
    ):
        """Initialize.

        :param app: web app
        :param session_service: session backend
        :param max_parallel_tasks: max number of tasks in the loop
        :param default_request_time: default request time in seconds if not specified by a header
        :param max_request_time: maximum allowed request time in seconds
        :param enable_permissions: enable perm checks in requests
        :param request_logs: log request body and also log responses (even successful ones)
        :param blacklist_routes: wildcard patterns to blacklist certain RPC routes
        :param blacklist_scope: integer value to blacklist permission scopes lower or equal to this value
        :param use_annotation_parser: annotation parser for non-validated method will be used and will try to
            create a method validator from its annotations
        :param logger:
        """
        ContextableService.__init__(self, app=app, logger=logger)
        self._sessions = session_service
        self._auth = auth_service
        self._max_parallel_tasks = max(1, int(max_parallel_tasks))
        self._default_request_time = max(1, int(default_request_time))
        self._max_request_time = max(self._default_request_time, int(max_request_time))
        self._enable_permissions = enable_permissions
        self._debug = self.app.debug
        self._request_logs = request_logs
        self._response_logs = response_logs
        self._blacklist_routes = blacklist_routes if blacklist_routes else []
        self._blacklist_scope = blacklist_scope
        self._use_annotation_parser = use_annotation_parser
        self._counter = self._max_parallel_tasks
        self._not_full = asyncio.Event()
        self._not_full.set()
        self._empty = asyncio.Event()
        self._empty.set()
        self._methods: Dict[str, MethodInfo] = {}

    async def init(self):
        if not self._enable_permissions:
            warnings.warn('Server permissions are disabled.')
        self._counter = self._max_parallel_tasks
        self._empty.set()
        self._not_full.set()
        self._sessions = self.discover_service(self._sessions, cls=SessionInterface, required=False)
        self._auth = self.discover_service(self._auth, cls=AuthenticationInterface, required=False)
        for service_name, service in self.app.services.items():
            if isinstance(service, PublicInterface):
                self.register_service(service_name, service)
        await super().init()

    async def close(self):
        await self._empty.wait()
        await super().close()

    @property
    def routes(self):
        return {'api': self.get_routes, 'status': self.get_status, 'tasks': self.get_tasks}

    @property
    def permissions(self):
        return {
            'api': self.PermissionKeys.GLOBAL_GUEST_PERMISSION,
            'status': self.PermissionKeys.GLOBAL_SYSTEM_PERMISSION,
            'tasks': self.PermissionKeys.GLOBAL_SYSTEM_PERMISSION,
        }

    @staticmethod
    async def get_tasks() -> list:
        """Get all current asyncio tasks."""
        tasks = asyncio.all_tasks(asyncio.get_running_loop())
        t = int(time())
        tasks_info = []
        for task in tasks:
            name = task.get_name()
            data = {'name': name}
            if name.startswith('rpc:'):
                task = cast(_Task, task)
                data.update(
                    {
                        'system': False,
                        'cid': name.split(':')[1],
                        'time_elapsed': t - task.started,
                        'time_left': task.deadline - task.started,
                    }
                )
            else:
                f_code = task.get_stack(limit=1)[-1].f_code
                data.update({'system': True, 'coro': f_code.co_name})
            tasks_info.append(data)

        tasks_info.sort(key=lambda o: (o['system'], o['name']))
        return tasks_info

    async def get_status(self) -> dict:
        """Get server status and current tasks."""
        return {
            'app': self.app.name,
            'app_id': self.app.id,
            'env': self.app.env,
            'debug': self._debug,
            'rpc_tasks': self._max_parallel_tasks - self._counter,
            'queue_full': not self._not_full.is_set(),
            'server_time': int(time()),
            'max_tasks': self._max_parallel_tasks,
            'max_timeout': self._max_request_time,
            'default_timeout': self._default_request_time,
            'enable_permissions': self._enable_permissions,
        }

    async def get_routes(self, pattern: str = '*') -> dict:
        """Get all RPC routes (you are here)."""
        session = self.get_session()
        routes = [
            {
                'route': route,
                'signature': method['signature'],
            }
            for route, method in self._methods.items()
            if session and method['permission'].value >= session.scope.value and fnmatch(route, pattern)
        ]
        routes.sort(key=lambda o: o['route'])
        return {'api': 'jsonrpc', 'version': JSONRPC, 'spec': 'https://www.jsonrpc.org/specification', 'routes': routes}

    def register_service(self, service_name: str, service: PublicInterface) -> None:
        """Register an RPC compatible service and its methods."""
        if not isinstance(service, PublicInterface):
            raise TypeError('Service must be rpc compatible.')
        permissions = service.permissions
        validators = service.validators
        for route, f in service.routes.items():
            full_name = f'{service_name}.{route}'
            if self._route_blacklisted(full_name):
                continue
            route_perm = PublicInterface.PermissionKeys.GLOBAL_SYSTEM_PERMISSION
            for pattern, perm in permissions.items():
                if fnmatch(route, pattern):
                    route_perm = perm
            if route_perm.value <= self._blacklist_scope:  # noqa
                continue
            try:
                annotation = AnnotationParser.parse_method(type(service), route, f)
            except Exception as exc:
                warnings.warn(f'Cannot automatically create validator for {route}: {exc}')
                annotation = None
            validator = None
            if route in validators:
                params = validators[route]
                if params:
                    if isinstance(params, Callable):
                        validator = params
                    else:
                        validator = compile_schema(params)
            elif self._use_annotation_parser and annotation:
                params = annotation['params']
                if params:
                    params = params.repr()
                    if params:
                        validator = compile_schema(params)
            # signature = inspect.signature(f)
            # sig_text = [str(value) for key, value in signature.parameters.items() if not key.startswith('_')]
            method = MethodInfo(
                f=f,
                permission=self._permission_levels[route_perm],
                validator=validator,
                service_name=service_name,
                signature=annotation,
            )
            self._methods[full_name] = method

    def _route_blacklisted(self, route: str) -> bool:
        """Check if route is blacklisted by this server instance."""
        for pattern in self._blacklist_routes:
            if fnmatch(route, pattern):
                return True
        return False

    async def call(
        self,
        body: Union[List, Dict],
        headers: dict = None,
        nowait: bool = False,
        callback: Callable[..., Awaitable] = None,
    ):
        """Call a server command.

        :param body: request body
        :param headers: request headers (optional)
        :param nowait: do not wait for the result
        :param callback: optional response callback which should contain (session, headers, result) input params
        """
        session = None
        if headers is None:
            headers = {}
        if self._sessions and headers.get(JSONRPCHeaders.SESSION_ID_HEADER):
            session = await self._sessions.load_session(headers[JSONRPCHeaders.SESSION_ID_HEADER])
        if not session and self._auth and JSONRPCHeaders.AUTHORIZATION in headers:
            try:
                session = await self._auth.header_auth(headers[JSONRPCHeaders.AUTHORIZATION])
            except NotAuthorized as exc:
                headers = self._get_request_headers(headers)
                headers = self._get_response_headers(headers['correlation_id'], session)
                return headers, RPCError(id=None, error=exc)

        scope = session.scope if session else Scope.GUEST
        headers = self._get_request_headers(headers)
        if type(body) in {list, tuple}:
            try:
                reqs = [
                    self._prepare_request(req, session, scope, n, use_template=headers['use_template'])
                    for n, req in enumerate(body)
                ]
                return_result = any(req[0] is not None for req in reqs)
            except JSONRPCError as exc:
                headers = self._get_response_headers(headers['correlation_id'], session)
                return headers, RPCError(id=exc.data.get('id'), error=exc)
            coro = self._execute_batch(
                reqs,
                retries=headers['retries'],
                request_deadline=headers['request_deadline'],
                abort_on_error=headers['abort_on_error'],
                use_template=headers['use_template'],
                session=session,
                correlation_id=headers['correlation_id'],
                callback=callback,
            )
        else:
            try:
                req_id, f, params, body = self._prepare_request(
                    body, session, scope, 0, use_template=headers['use_template']
                )
                return_result = req_id is not None
            except JSONRPCError as exc:
                headers = self._get_response_headers(headers['correlation_id'], session)
                return headers, RPCError(id=exc.data.get('id'), error=exc)
            coro = self._execute_single(
                f,
                params,
                request_id=req_id,
                body=body,
                retries=headers['retries'],
                request_deadline=headers['request_deadline'],
                session=session,
                correlation_id=headers['correlation_id'],
                callback=callback,
            )
        self._counter -= 1
        if not self._not_full.is_set():
            await self._not_full.wait()
        task = asyncio.create_task(coro)
        task.set_name(f'rpc:{headers["correlation_id"]}')
        setattr(task, 'deadline', headers['request_deadline'])
        setattr(task, 'started', int(time()))
        task.add_done_callback(self._request_done_cb)
        if self._empty.is_set():
            self._empty.clear()
        if self._counter <= 0:
            self._counter = 0
            self._not_full.clear()
        if not return_result:
            return self._get_response_headers(headers['correlation_id'], session), None
        elif nowait:
            return headers, task
        else:
            return await task

    @staticmethod
    def _get_int_header(value: Union[str, None], default) -> int:
        """Parse an integer header value.

        https://httpwg.org/specs/rfc8941.html#integer
        """
        try:
            return int(value) if value else default
        except ValueError:
            return default

    @staticmethod
    def _get_bool_header(value: Union[str, bool, None], default: bool) -> bool:
        """Parse a boolean header value.

        https://httpwg.org/specs/rfc8941.html#boolean
        """
        if type(value) is bool:
            return value
        return value == '?1' if value else default

    def _get_request_headers(self, headers: Union[dict, None]) -> RequestHeaders:
        if headers is None:
            headers = {}
        request_deadline = headers.get(JSONRPCHeaders.REQUEST_DEADLINE_HEADER)
        t0 = int(time())
        if request_deadline:
            request_deadline = min(self._get_int_header(request_deadline, 0), t0 + self._max_request_time)
        else:
            request_timeout = headers.get(JSONRPCHeaders.REQUEST_TIMEOUT_HEADER)
            request_timeout = min(
                self._max_request_time, max(1, self._get_int_header(request_timeout, self._default_request_time))
            )
            request_deadline = t0 + request_timeout + 1
        correlation_id = headers.get(JSONRPCHeaders.CORRELATION_ID_HEADER)
        if not correlation_id:
            correlation_id = b2a_hex(os.urandom(4)).decode()
        return RequestHeaders(
            correlation_id=correlation_id,
            request_deadline=request_deadline,
            abort_on_error=self._get_bool_header(headers.get(JSONRPCHeaders.ABORT_ON_ERROR), False),
            use_template=self._get_bool_header(headers.get(JSONRPCHeaders.USE_TEMPLATE), False),
            retries=min(10, max(0, self._get_int_header(headers.get(JSONRPCHeaders.RETRIES), 0))),
        )

    async def _execute_single(
        self,
        f: Callable,
        params: dict,
        request_id: _RequestId,
        body: dict,
        retries: int,
        request_deadline: int,
        session: Optional[Session],
        correlation_id: Optional[str],
        callback: Callable[..., Awaitable],
    ) -> Tuple[dict, Union[RPCResponse, RPCError]]:
        """Execute a single rpc request."""
        ctx = RequestContext(
            session_id=session.id if session else None,
            request_deadline=request_deadline,
            correlation_id=correlation_id,
        )
        REQUEST_SESSION.set(session)
        REQUEST_CONTEXT.set(ctx)
        try:
            async with timeout(request_deadline - time()):
                result = await self._execute_request(f, params, retries, request_id, body)
        except asyncio.TimeoutError:
            result = RPCError(
                id=request_id, error=RequestTimeout(message='Request timeout', request_deadline=request_deadline)
            )
        session = self.get_session()
        if self._sessions and session and session.stored and session.changed:
            await self._sessions.save_session(session)
        if result.id is not None or type(result) is not RPCResponse:
            headers = self._get_response_headers(correlation_id, session)
            if callback:
                cb = asyncio.create_task(callback(session, headers, result))  # noqa
                cb.set_name(f'rpc:{correlation_id}:callback')
            return headers, result

    @staticmethod
    def _get_response_headers(correlation_id: str, session: Optional[Session]) -> dict:
        headers = {}
        if correlation_id:
            headers[JSONRPCHeaders.CORRELATION_ID_HEADER] = correlation_id
        if session and session.stored and (session.changed or session.loaded):
            headers[JSONRPCHeaders.SESSION_ID_HEADER] = session.id
        return headers

    async def _execute_batch(
        self,
        requests: List[Tuple[_RequestId, Callable, dict, dict]],
        retries: int,
        request_deadline: int,
        abort_on_error: bool,
        use_template: bool,
        session: Optional[Session],
        correlation_id: Optional[str],
        callback: Callable[..., Awaitable],
    ) -> Tuple[dict, List[Union[RPCResponse, RPCError]]]:
        """Execute multiple coroutine functions."""
        ctx = RequestContext(
            session_id=session.id if session else None,
            request_deadline=request_deadline,
            correlation_id=correlation_id,
        )
        REQUEST_SESSION.set(session)
        REQUEST_CONTEXT.set(ctx)
        results, template_ctx, req_id = [], {}, None
        for n, (req_id, f, params, body) in enumerate(requests):
            try:
                if use_template:
                    if n > 0:
                        params = Template(params).fill(template_ctx)
                    method = self._methods[body['method']]
                    if method['validator']:
                        params = method['validator'](params)
                async with timeout(request_deadline - time()):
                    result = await self._execute_request(f, params, retries, req_id, body)
                if abort_on_error and isinstance(result, RPCError):
                    raise _Aborted
                if use_template and req_id is not None and type(result) is RPCResponse:
                    template_ctx[str(req_id)] = result.result
            except asyncio.TimeoutError:
                results.extend(
                    (
                        RPCError(
                            id=req_id,
                            error=RequestTimeout(message='Request timeout', request_deadline=request_deadline),
                        )
                        for req_id, f, params, body in requests[n:]
                    )
                )
                break
            except Exception as exc:
                self.logger.error('Batch error', batch_num=n, request_id=req_id, exc_info=exc)
                results.extend(
                    (RPCError(id=req_id, error=Aborted(message='Aborted')) for req_id, f, params, body in requests[n:])
                )
                break
            else:
                if result.id is not None or type(result) is not RPCResponse:
                    results.append(result)
        session = self.get_session()
        if self._sessions and session and session.stored and session.changed:
            await self._sessions.save_session(session)
        headers = self._get_response_headers(correlation_id, session)
        if results:
            if callback:
                cb = asyncio.create_task(callback(session, headers, results))  # noqa
                cb.set_name(f'rpc:{correlation_id}:callback')
            return headers, results

    def _prepare_request(
        self, body, session: Optional[Session], scope: Scope, default_id: int, use_template: bool
    ) -> (_RequestId, Callable, dict, dict):
        """Pre-validate and prepare request for the execution."""
        # request body validation
        if type(body) is not dict:
            raise InvalidRequest(id=None, message='Request must be an object')
        if 'id' not in body:
            body['id'] = _id = default_id
        else:
            _id = body['id']
            if _id is not None and type(_id) is not int:
                raise InvalidRequest(id=None, message='Request "id" must be an integer or null', request_id=_id)

        # method visibility check

        method_name = body.get('method')
        if not method_name:
            raise InvalidRequest(id=_id, message='Request "method" must be a string', request_method=method_name)
        try:
            method = self._methods[method_name]
        except KeyError:
            raise MethodNotFound(id=_id, message='Method not found', request_method=method_name) from None
        else:
            if self._enable_permissions:
                if all(
                    (
                        method['permission'].value < scope.value,
                        not session or method_name not in session.permissions,
                        not session or method['service_name'] not in session.permissions,
                    )
                ):
                    raise PermissionDenied(id=_id, message='Method not found', request_method=method_name)

        # request params validation

        params = body.get('params')
        if params is None:
            params = {}
        if not type(params) is dict:
            raise InvalidParams(id=_id, message='Request "params" must be an object', request_params=params)
        if params:
            params = {k: v for k, v in params.items() if not k.startswith('_')}
            if not use_template and method['validator']:  # template validation is postponed
                try:
                    params = method['validator'](params)
                except Exception as exc:
                    raise InvalidParams(id=_id, message=str(exc), base_exc=exc)

        return _RequestId(_id), method['f'], params, body

    async def _execute_request(
        self,
        f: Callable,
        params: dict,
        retries: int,
        request_id: _RequestId,
        request: dict,
    ) -> Union[RPCResponse, RPCError]:
        """Execute a coro and process an exception."""
        t0 = time()
        try:
            if retries:
                result = await retry(f, kws=params, retries=retries, logger=self.logger)
            else:
                result = await f(**params)
        except ClientError as exc:
            result = RPCError(id=request_id, error=exc)
            self.logger.info('Client error', result=exc)
        except APIException as exc:
            result = RPCError(id=request_id, error=exc)
            self.logger.error('Internal error', request=request, exc_info=exc)
        except Exception as exc:
            result = RPCError(id=request_id, error=InternalError(base_exc=exc, message='Internal error'))
            self.logger.error('Internal error', request=request, exc_info=exc)
        else:
            result = RPCResponse(id=request_id, result=result)
            if self._response_logs:
                self.logger.info('request', request=request, result=result.result, took_ms=int((time() - t0) * 1000))
            elif self._request_logs:
                self.logger.info('request', request=request, took_ms=int((time() - t0) * 1000))
        return result

    def _request_done_cb(self, task: asyncio.Task) -> None:
        """Increment the counter when a request is finished."""
        self._counter += 1
        if self._counter >= self._max_parallel_tasks:
            self._counter = self._max_parallel_tasks
            self._empty.set()
        if not self._not_full.is_set():
            self._not_full.set()
        exc = task.exception()
        if exc:
            self.logger.error('task execution error', exc_info=exc)


class BaseRPCClient(ContextableService, RPCClient, abc.ABC):
    """JSONRPC client."""

    transport_cls = Service

    class Topic(Enum):
        """Default topic names."""

        RPC = 'rpc'
        MANAGER = 'manager'
        EXECUTOR = 'executor'

    def __init__(
        self,
        *args,
        transport: str,
        request_logs: bool = True,
        response_logs: bool = False,
        auth_str: str = None,
        scheduler: Scheduler = None,
        token_client: TokenClientService = False,
        **kws,
    ):
        super().__init__(*args, **kws)
        self._transport = transport
        self._scheduler = scheduler
        self._request_logs = request_logs
        self._response_logs = response_logs
        self._auth_str = auth_str
        self._token_client = token_client

    async def init(self):
        self._transport = self.discover_service(self._transport, cls=self.transport_cls)
        self._token_client = self.discover_service(self._token_client, cls=TokenClientService, required=False)

    async def call(
        self,
        method: str,
        params: Union[dict, None] = None,
        nowait: bool = False,
        request_id: int = 0,
        max_timeout: int = None,
        use_context: bool = True,
    ) -> Union[Any, None]:
        """Make an RPC call.

        :param method: rpc method name
        :param params: method call arguments
        :param nowait: create a 'notify' request - do not wait for the result
        :param request_id: optional request id (usually you don't need to set it)
        :param max_timeout: request timeout in sec
        :param use_context: use app request context such as correlation id and request chain deadline
        """
        t0 = time()
        headers = self._create_request_headers(max_timeout, use_context, nowait)
        _id = None if nowait else request_id
        body = RPCRequest(id=_id, method=method, params=params)
        response = await self._request(body, headers)
        result = self._process_response(response) if response else None
        if isinstance(result, Exception):
            raise result
        if self._response_logs:
            self.logger.info('request', request=body, result=response, took_ms=int((time() - t0) * 1000))
        elif self._request_logs:
            self.logger.info('request', request=body, took_ms=int((time() - t0) * 1000))
        return result

    async def call_multiple(
        self,
        *requests: dict,
        raise_exception: bool = True,
        nowait: bool = False,
        max_timeout: int = None,
        use_context: bool = True,
    ) -> Union[List, None]:
        """Make an RPC batch call.

        :param requests: list of request dicts
        :param nowait: create a 'notify' request - do not wait for the result
        :param max_timeout: request timeout in sec
        :param use_context: use app request context such as correlation id and request chain deadline
        :param raise_exception: raise exception instead of returning error objects in the list
        """
        headers = self._create_request_headers(max_timeout, use_context, nowait)
        body = [RPCRequest(id=n, **req) for n, req in enumerate(requests)]
        response = await self._request(body, headers)
        if response is None:  # for notify requests
            return
        results = []
        for resp in response:
            resp = self._process_response(resp)
            if isinstance(resp, Exception) and raise_exception:
                raise resp
            results.append(resp)
        return results

    @abc.abstractmethod
    async def _request(self, body: Union[RPCRequest, List[RPCRequest]], headers: dict):
        """Make an external requests via transport service."""

    def _create_request_headers(self, max_timeout, use_context, nowait) -> dict:
        headers = {}
        ctx = REQUEST_CONTEXT.get() if use_context else None
        if ctx:
            headers[JSONRPCHeaders.CORRELATION_ID_HEADER] = ctx['correlation_id']
            if not nowait:
                headers[JSONRPCHeaders.REQUEST_DEADLINE_HEADER] = ctx['request_deadline']
        else:
            headers[JSONRPCHeaders.CORRELATION_ID_HEADER] = get_short_uid()
        if max_timeout:
            headers[JSONRPCHeaders.REQUEST_TIMEOUT_HEADER] = max_timeout
        if self._auth_str:
            headers[JSONRPCHeaders.AUTHORIZATION] = self._auth_str
        elif self._token_client:
            token = self._token_client.get_token()
            if token:
                headers[JSONRPCHeaders.AUTHORIZATION] = f'Bearer {token}'
        return headers

    def _process_response(self, response: dict):
        if 'error' in response:
            return self._create_exception(response['error'])
        else:
            return response['result']

    @staticmethod
    def _create_exception(error_data: dict) -> RPCClientError:
        exc = RPCClientError(message=error_data['message'], data=error_data['data'])
        exc.status_code = error_data['code']
        return exc
