"""HTTP services and classes."""

import asyncio
import logging
from pathlib import Path
from time import time
from typing import Union, List, cast

from aiohttp import BasicAuth
from aiohttp_cors import CorsViewMixin
from aiohttp.client import ClientSession, TCPConnector, ClientResponseError
from aiohttp.cookiejar import CookieJar
from aiohttp.http_websocket import WSMessage
from aiohttp.web import Request, Response, View, json_response, WebSocketResponse, WSMsgType, middleware
from aiohttp.web_exceptions import HTTPClientError

from kaiju_tools.interfaces import SessionInterface, App
from kaiju_tools.types import Session, Scope
from kaiju_tools.rpc import BaseRPCClient, RPCRequest, RPCError, JSONRPCServer, JSONRPCHeaders
from kaiju_tools.exceptions import HTTPRequestError, InternalError, ClientError
from kaiju_tools.app import ContextableService
from kaiju_tools.serialization import dumps, loads
from kaiju_tools.sessions import AuthenticationService, SessionService

__all__ = [
    'HTTPService',
    'RPCClientService',
    'error_middleware',
    'JSONRPCView',
    'RPCClientService',
    'session_middleware',
]


class HTTPService(ContextableService):
    """HTTP transport."""

    UPLOAD_CHUNK_SIZE = 4096 * 1024

    def __init__(
        self,
        app,
        *,
        host: str = 'http://localhost:80',
        headers: dict = None,
        session: ClientSession = None,
        conn_settings: dict = None,
        auth: Union[dict, str] = None,
        cookie_settings: dict = None,
        request_logs: bool = False,
        response_logs: bool = False,
        logger: logging.Logger = None,
    ):
        """Initialize.

        :param app:
        :param host: full hostname
        :param headers: default request headers
        :param session: session object
        :param conn_settings: session connection settings
        :param auth: basic auth settings — "login", "password" and
            (optional) "encoding" (ignored if a session has been passed)
            or pass a single string which goes directly into the authorization header.
        :param cookie_settings:
        :param response_logs: log responses
        :param logger: a logger for a super class
        :param request_logs: enable request logs
        """
        super().__init__(app=app, logger=logger)
        self.host = host.rstrip('/')
        if session is None:
            if headers is None:
                headers = {}
            if isinstance(auth, str):
                headers['Authorization'] = auth
                auth = None
            elif isinstance(auth, dict):
                auth = BasicAuth(**auth)
            if cookie_settings is None:
                cookie_settings = {}
            if conn_settings is None:
                conn_settings = {}
            connector = TCPConnector(verify_ssl=False, limit=256, ttl_dns_cache=60)
            session = ClientSession(
                connector=connector,
                cookie_jar=CookieJar(**cookie_settings),
                headers=headers,
                json_serialize=dumps,
                raise_for_status=False,
                auth=auth,
                **conn_settings,
            )
        self.session = session
        self._request_logs = request_logs
        self._response_logs = response_logs

    async def init(self):
        pass

    async def close(self):
        if not self.closed:
            await self.session.close()

    async def upload_file(self, uri: str, file: Union[Path, str], method: str = 'post', chunk_size=UPLOAD_CHUNK_SIZE):
        """Upload file to a remote location."""
        """Upload a file."""

        def _read_file(path):
            with open(path, 'rb') as f:
                chunk = f.read(chunk_size)
                while chunk:
                    yield chunk
                    chunk = f.read(chunk_size)

        if type(file) is str:
            file = Path(file)
        result = await self.request(method=method, uri=uri, data=_read_file(file))
        return result

    async def request(
        self,
        method: str,
        uri: str,
        *,
        data=None,
        json=None,
        params=None,
        headers=None,
        accept_json: bool = True,
        **kws,
    ) -> dict:
        """Make a http rest request."""
        url = self.resolve(uri)
        if params:
            params = {str(k): str(v) for k, v in params.items()}
        if self._request_logs:
            record = json if json else '[BYTES]'
            self.logger.info('Request', method=method, url=url, params=params, body=record)
        if headers:
            headers = {k: str(v) for k, v in headers.items()}
        t0 = time()
        async with self.session.request(
            method,
            url,
            params=params,
            headers=headers,
            data=data,
            # cookies=self.session.cookie_jar._cookies,  # noqa ? pycharm
            json=json,
            **kws,
        ) as response:
            response.encoding = 'utf-8'
            text = await response.text()
            t = int((time() - t0) * 1000)
            if response.status >= 400:
                try:
                    text = loads(text)
                except ValueError:
                    text = None
                exc = ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                )
                exc.params = params
                exc.took_ms = t
                exc.request = json if json else None
                exc.response = text
                raise HTTPRequestError(base_exc=exc, message=str(exc))

        if text is not None and accept_json:
            text = loads(text)
        if self._response_logs:
            self.logger.info(
                'Response',
                method=method,
                url=url,
                params=params,
                status=response.status,
                body=text if accept_json else '[BYTES]',
                took_ms=t,
            )
        return text

    def resolve(self, uri: str) -> str:
        return f"{self.host}/{uri.lstrip('/')}"


class RPCClientService(BaseRPCClient):
    """HTTP JSONRPC client service."""

    transport_cls = HTTPService
    _transport: HTTPService

    def __init__(self, *args, base_uri: str = '/public/rpc', **kws):
        """Initialize."""
        super().__init__(*args, **kws)
        self.base_uri = base_uri

    async def _request(self, body: Union[RPCRequest, List[RPCRequest]], headers: dict):
        """Make a HTTP request."""
        return await self._transport.request('post', self.base_uri, json=body, headers=headers)


@middleware
async def error_middleware(request: Request, handler):
    """Wrap an error in RPC exception."""
    try:
        response = await handler(request)
    except HTTPClientError as exc:
        error = ClientError(message=str(exc), base_exc=exc)
        request.app.logger.error(str(exc))
        return json_response(RPCError(id=None, error=error), dumps=dumps)
    except Exception as exc:
        error = InternalError(message='Internal error', base_exc=exc)
        request.app.logger.error(str(exc), exc_info=exc)
        return json_response(RPCError(id=None, error=error), dumps=dumps)
    else:
        return response


@middleware
async def session_middleware(request: Request, handler):
    app = cast(App, request.app)
    headers = request.headers
    if JSONRPCHeaders.SESSION_ID_HEADER in headers:
        request['session_id'] = headers[JSONRPCHeaders.SESSION_ID_HEADER]
        return await handler(request)
    else:
        cookie_key = f'{app.env}-{app.name}-sid'
        session_id = request.cookies.get(cookie_key)
        if session_id:
            request['session_id'] = session_id
        response = await handler(request)
        new_session_id = response.headers.get(JSONRPCHeaders.SESSION_ID_HEADER, '')
        if session_id != new_session_id:
            response.set_cookie(cookie_key, new_session_id, secure=not request.app.debug, httponly=True)  # noqa
        return response


# async def jsonrpc_websocket_handler(
#     request: Request, rpc_server_name: str = None, session_service_name: str = None, validate_session: bool = True
# ):
#     """Read from websocket."""
#     ws = WebSocketResponse()
#     counter = 0
#     services: ServiceContextManager = request.app.services  # noqa
#     rpc: JSONRPCServer = services.discover_service(rpc_server_name, cls=JSONRPCServer)
#     sessions: SessionInterface = services.discover_service(session_service_name, cls=SessionInterface)
#     session: Session = request.get('session', None)
#     scope: Scope = session.scope if session else Scope.GUEST
#     headers = dict(request.headers)
#
#     async def _send_response(_session: Session, headers: dict, result):  # noqa
#         nonlocal session, scope, request
#         session = request['session'] = _session
#         scope = session.scope
#         await ws.send_json(result.repr(), dumps=dumps)
#
#     await ws.prepare(request)
#
#     try:
#         async for msg in ws:
#             msg = cast(WSMessage, msg)
#             if msg.type == WSMsgType.ERROR:
#                 request.app.logger.error('Websocket error: %s', ws.exception())
#             elif msg.type == WSMsgType.TEXT:
#                 if msg.data == 'close':
#                     await ws.close()
#                     break
#
#                 if validate_session:
#                     session_exists = await sessions.session_exists(session.id)
#                     if not session_exists:
#                         session = None  # noqa
#                         del request['session']
#                         await ws.close()
#                         break
#
#                 data = loads(msg.data)
#                 counter += 1
#                 if 'id' not in data:
#                     data['id'] = counter
#                 result = await rpc.call(
#                     data, headers=headers, session=session, scope=scope, nowait=True, callback=_send_response
#                 )
#                 if type(result) is not asyncio.Task:
#                     _headers, result = result
#                     if result:
#                         await ws.send_json(result, dumps=dumps)
#     except Exception as exc:
#         request.app.logger.error('Websocket error', exc_info=exc)
#
#     finally:
#         ws._headers[JSONRPCHeaders.SESSION_ID_HEADER] = session.id if session else ''  # noqa
#         if not ws.closed:
#             await ws.close()
#         return ws


class JSONRPCView(CorsViewMixin, View):
    """JSON RPC server endpoint."""

    route = '/public/rpc'

    async def post(self):
        """Make an RPC request."""
        if not self.request.can_read_body:
            return Response()
        app = cast(App, self.request.app)
        rpc = cast(JSONRPCServer, app.services['rpc'])
        headers = dict(self.request.headers)
        session_id = self.request.get('session_id')
        if session_id:
            headers[JSONRPCHeaders.SESSION_ID_HEADER] = session_id
        data = await self.request.json(loads=loads)
        headers, result = await rpc.call(data, headers=headers, nowait=False)
        return json_response(result, headers=headers, dumps=dumps)
