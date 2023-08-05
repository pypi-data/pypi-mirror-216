import asyncio
import logging
import uuid
from datetime import datetime
from time import time
from typing import cast, Dict, List, FrozenSet, Optional, Collection, Hashable, Type, AsyncGenerator, Union

import pytest  # noqa: pycharm
import pytest_asyncio

import kaiju_tools.jsonschema as js
from kaiju_tools.exceptions import ValidationError, NotFound
from kaiju_tools.app import (
    HandlerSettings,
    LoggerSettings,
    LoggingService,
    ServiceContextManager,
    REQUEST_CONTEXT,
    REQUEST_SESSION,
    Scheduler,
    Service,
)
from kaiju_tools.interfaces import DataStore, UserInterface, TokenInterface, _Columns, _Row, _User, App  # noqa
from kaiju_tools.rpc import JSONRPCServer, AbstractRPCCompatible
from kaiju_tools.cache import BaseCacheService
from kaiju_tools.locks import BaseLocksService, NotLockOwnerError, LockExistsError
from kaiju_tools.sessions import SessionService, AuthenticationService, LoginService
from kaiju_tools.templates import Condition
from kaiju_tools.types import NSKey, TTLDict, Namespace, Session
from kaiju_tools.streams import Listener, StreamRPCClient
from kaiju_tools.http import error_middleware

__all__ = [
    'logger',
    'app',
    'rpc',
    'scheduler',
    'mock_cache',
    'mock_locks',
    'mock_service',
    'mock_session',
    'mock_sessions',
    'get_app',
    'mock_auth',
    'mock_tokens',
    'mock_users',
    'mock_data_store',
    'mock_listener',
    'mock_stream_client',
    'mock_login',
]


@pytest.fixture(scope='session')
def logger():
    """Get a test logger preconfigured to DEBUG level."""
    logger = logging.getLogger('pytest')
    logger.setLevel('DEBUG')
    return logger


def get_app(logger) -> App:
    from aiohttp.web import Application

    app = Application(middlewares=[error_middleware], logger=logger, debug=True)
    app.id = str(uuid.uuid4())
    app.name = 'pytest'
    app.env = 'pytest'
    app.namespace = Namespace(env=app.env, name=app.name)
    app.namespace_shared = Namespace(env=app.env, name='__shared__')
    app.request_context = REQUEST_CONTEXT
    app.request_session = REQUEST_SESSION
    app = cast(App, app)
    app.services = ServiceContextManager(app, settings=[], logger=logger)
    logger_settings = [LoggerSettings(name='root', enabled=True, handlers=['default'], loglevel='DEBUG')]
    handler_settings = [
        HandlerSettings(cls='StreamHandler', name='default', enabled=True, formatter='TextFormatter', loglevel='DEBUG')
    ]
    logging_service = LoggingService(
        app=app, handlers=handler_settings, loggers=logger_settings, loglevel='DEBUG', logger=logger
    )
    app.services.add_service(logging_service)
    app.cleanup_ctx.append(app.services.cleanup_context)
    return app


@pytest.fixture
def app(logger) -> App:
    """Create a web app.

    Depends on:

        aiohttp
    """
    return get_app(logger)


@pytest.fixture
def rpc(app) -> JSONRPCServer:
    service = JSONRPCServer(app=app, request_logs=True, response_logs=True)
    app.services.add_service(service)
    return service


@pytest.fixture
def scheduler(app) -> Scheduler:
    service = Scheduler(app=app, refresh_rate=0.1)
    app.services.add_service(service)
    return service


class _MockDataStore(Service, DataStore):
    def __init__(self, *args, primary_key: Union[str, List[str]] = 'id', **kws):
        super().__init__(*args, **kws)
        self.primary_key = primary_key
        self._ext = {}

    def _get_primary_key(self, row: dict):
        if type(self.primary_key) is str:
            return row[self.primary_key]
        else:
            return tuple(row[key] for key in self.primary_key)

    @staticmethod
    def _filter_columns(row: dict, columns) -> Optional[dict]:
        if not columns:
            return
        elif columns == '*':
            return row
        else:
            return {key: row[key] for key in row if key in columns}

    @staticmethod
    def _check_condition(row: dict, conditions: Optional[Condition]) -> bool:
        return conditions(row) if conditions else True

    async def get(self, id: Hashable, columns: _Columns = '*', _connection=None) -> _Row:
        await asyncio.sleep(0)
        try:
            row = self._ext[id]
        except KeyError:
            raise NotFound
        else:
            return self._filter_columns(row, columns)

    async def m_get(self, id: Collection[Hashable], columns: _Columns = '*', _connection=None) -> Collection[_Row]:
        await asyncio.sleep(0)
        rows = [self._ext.get(key) for key in id if key in self._ext]
        return [self._filter_columns(row, columns) for row in rows]

    async def exists(self, id: Hashable, _connection=None) -> bool:
        await asyncio.sleep(0)
        return id in self._ext

    async def m_exists(self, id: Collection[Hashable], _connection=None) -> FrozenSet[Hashable]:
        await asyncio.sleep(0)
        return frozenset(key for key in id if key in self._ext)

    async def delete(self, id: Hashable, columns: _Columns = None, _connection=None) -> _Row:
        await asyncio.sleep(0)
        try:
            row = self._ext.pop(id)
        except KeyError:
            raise NotFound
        else:
            if columns:
                return self._filter_columns(row, columns)

    async def m_delete(
        self, id: Collection[Hashable] = None, conditions=None, columns: _Columns = None, _connection=None
    ) -> Collection[_Row]:
        await asyncio.sleep(0)
        if conditions:
            conditions = Condition(conditions)
        rows = []
        keys = id if id else tuple(self._ext.keys())
        for key in keys:
            if key in self._ext and self._check_condition(self._ext[key], conditions):
                row = self._ext.pop(key)
                rows.append(self._filter_columns(row, columns))
        if columns:
            return rows

    async def create(
        self,
        data: dict,
        columns: _Columns = '*',
        _connection=None,
        on_conflict: str = None,
        on_conflict_keys: Collection = None,
        on_conflict_values=None,
    ) -> _Row:
        await asyncio.sleep(0)
        self._ext[self._get_primary_key(data)] = data
        if columns:
            return self._filter_columns(data, columns)

    async def m_create(
        self,
        data: Collection,
        columns: _Columns = '*',
        _connection=None,
        on_conflict: str = None,
        on_conflict_keys: Collection = None,
        on_conflict_values: dict = None,
    ) -> Collection[_Row]:
        await asyncio.sleep(0)
        rows = []
        for row in data:
            self._ext[self._get_primary_key(row)] = row
            rows.append(self._filter_columns(row, columns))
        if columns:
            return rows

    async def update(self, id: Hashable, data, columns: _Columns = '*', _connection=None) -> _Row:
        try:
            self._ext[id].update(data)
        except KeyError:
            raise NotFound
        else:
            if columns:
                return self._filter_columns(self._ext[id], columns)

    async def m_update(
        self, id: Collection[Hashable], data, conditions=None, columns: _Columns = '*', _connection=None
    ) -> Collection[_Row]:
        if conditions:
            conditions = Condition(conditions)
        rows = []
        keys = id if id else tuple(self._ext.keys())
        for key in keys:
            if key in self._ext and self._check_condition(self._ext[key], conditions):
                self._ext[key].update(data)
                row = self._ext[key]
                rows.append(self._filter_columns(row, columns))
        if columns:
            return rows

    async def iter(
        self, conditions: dict = None, sort=None, offset: int = 0, limit: int = 10, columns: _Columns = '*'
    ) -> AsyncGenerator[List[dict], None]:
        if conditions:
            conditions = Condition(conditions)
        rows = [
            self._filter_columns(row, columns) for row in self._ext.values() if self._check_condition(row, conditions)
        ][offset:]
        for _offset in range(0, (len(rows) // limit) + 1):
            chunk = rows[_offset * limit : (_offset + 1) * limit]
            if chunk:
                yield chunk


@pytest.fixture
def mock_data_store(app) -> _MockDataStore:
    service = _MockDataStore(app=app)
    app.services.add_service(service)
    return service


class _MockCacheService(BaseCacheService):
    class MockTransport(Service):
        pass

    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)
        self._ext = TTLDict()

    @classmethod
    def get_transport_cls(cls) -> Type:
        return cls.MockTransport

    async def exists(self, id: NSKey) -> bool:
        return id in self._ext

    async def m_exists(self, id: NSKey):
        return frozenset([key for key in id if key in self._ext])

    async def _get(self, key: NSKey):
        return self._ext.get(key)

    async def _m_get(self, *keys: NSKey) -> List[NSKey]:
        return [self._ext.get(key) for key in keys]

    async def _set(self, key: NSKey, value: bytes, ttl: int):
        self._ext.set(key, value, ttl)

    async def _m_set(self, keys: Dict[NSKey, bytes], ttl: int):
        for key, value in keys.items():
            self._ext.set(key, value, ttl)

    async def _delete(self, key: str):
        if key in self._ext:
            del self._ext[key]

    async def _m_delete(self, *keys: NSKey):
        for key in keys:
            await self._delete(key)


@pytest.fixture
def mock_cache(app) -> _MockCacheService:
    service = _MockCacheService(app=app, transport=_MockCacheService.MockTransport(app))
    app.services.add_service(service)
    return service


@pytest.fixture
def mock_sessions(app, mock_cache, mock_data_store) -> SessionService:
    service = SessionService(app=app, cache_service=mock_cache, session_store=mock_data_store)
    app.services.add_service(service)
    return service


@pytest_asyncio.fixture
async def mock_session(mock_sessions) -> Session:
    _session = Session(
        id='mock_session',
        user_id=uuid.uuid4(),
        permissions=frozenset({'mock_permission', 'user'}),
        data={},
        created=datetime.now(),
        h_agent=None,
        expires=int(time() + 1000),
        _stored=True,
        _changed=False,
        _loaded=False,
    )
    _session._changed = True
    await mock_sessions.save_session(_session)
    _session._changed = False
    return _session


class _MockTokenService(Service, TokenInterface):
    token: str
    refresh_token: str
    user_id: uuid.UUID
    permissions: frozenset

    def __init__(self, *args, session: Session, **kws):
        super().__init__(*args, **kws)
        self.token = uuid.uuid4().hex
        self.refresh_token = uuid.uuid4().hex
        self.user_id = session.user_id
        self.permissions = session.permissions

    async def auth(self, token: str, /) -> Optional[TokenInterface.TokenClaims]:
        if token == self.token:
            return TokenInterface.TokenClaims(id=self.user_id, permissions=self.permissions)

    async def get(self, claims: TokenInterface.TokenClaims, /) -> TokenInterface.TokenInfo:
        return TokenInterface.TokenInfo(access=self.token, refresh=self.refresh_token)

    async def refresh(self, token: str, /) -> Optional[TokenInterface.TokenInfo]:
        if token == self.refresh_token:
            return TokenInterface.TokenInfo(access=self.token, refresh=self.refresh_token)


@pytest.fixture
def mock_tokens(app, mock_session) -> TokenInterface:  # noqa: pycharm
    service = _MockTokenService(app=app, session=mock_session)
    app.services.add_service(service)
    return service


class _MockUserService(Service, UserInterface):
    def __init__(self, *args, session: Session, **kws):
        super().__init__(*args, **kws)
        self.username = uuid.uuid4().hex
        self.password = uuid.uuid4().hex
        self.session = session

    async def auth(self, username: str, password: str) -> Optional[_User]:
        if username == self.username and password == self.password:
            return TokenInterface.TokenClaims(id=self.session.user_id, permissions=self.session.permissions)


@pytest.fixture
def mock_users(app, mock_session) -> _MockUserService:  # noqa: pycharm
    service = _MockUserService(app=app, session=mock_session)
    app.services.add_service(service)
    return service


@pytest.fixture
def mock_auth(app, mock_sessions, mock_users, mock_tokens) -> AuthenticationService:
    service = AuthenticationService(
        app=app,
        session_service=mock_sessions,
        user_service=mock_users,
        token_service=mock_tokens,
        enable_token_auth=True,
        enable_basic_auth=True,
    )
    app.services.add_service(service)
    return service


@pytest.fixture
def mock_login(app, rpc, mock_sessions, mock_users, mock_auth, mock_tokens) -> LoginService:
    service = LoginService(app=app)
    app.services.add_service(service)
    return service


class _MockLockService(BaseLocksService):
    class MockTransport(Service):
        pass

    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)
        self._ext = TTLDict()

    @classmethod
    def get_transport_cls(cls) -> Type:
        return cls.MockTransport

    async def m_exists(self, keys: List[NSKey]) -> FrozenSet[NSKey]:
        s = frozenset(key for key in keys if key in self._ext)
        return s

    async def _acquire(self, keys: List[NSKey], identifier, ttl: int):
        for key in keys:
            if key in self._ext:
                raise LockExistsError(key)
        for key in keys:
            self._ext.set(key, identifier, ttl=ttl)

    async def _release(self, keys: List[NSKey], identifier) -> None:
        for key in keys:
            existing = self._ext.get(key)
            if existing and existing != identifier:
                raise NotLockOwnerError()
            del self._ext[key]

    async def _renew(self, keys: List[NSKey], values: List[int]) -> None:
        for key, ttl in zip(keys, values):
            existing = self._ext.get(key)
            if existing:
                self._ext.set(key, existing, ttl=ttl)

    async def _owner(self, key: NSKey):
        return self._ext.get(key)


@pytest.fixture
def mock_locks(app, scheduler) -> _MockLockService:
    service = _MockLockService(app=scheduler.app, transport=_MockLockService.MockTransport(scheduler.app))
    app.services.add_service(service)
    return service


class _MockService(Service, AbstractRPCCompatible):
    """Mocked service with RPC interface."""

    service_name = 'do'

    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)
        self.retry_counter = 0
        self.stored = None

    @property
    def routes(self) -> dict:
        return {
            'guest': self.guest,
            'echo': self.echo,
            'echo_validated': self.echo_validated,
            'echo_custom_validated': self.echo_custom_validated,
            'echo_user': self.echo_user,
            'echo_session': self.echo_session,
            'write_session': self.write_session,
            'call_system_method': self.call_system_method,
            'fail': self.fail,
            'retry': self.retry,
            'store': self.store,
        }

    @property
    def permissions(self) -> dict:
        return {
            '*': self.PermissionKeys.GLOBAL_USER_PERMISSION,
            'guest': self.PermissionKeys.GLOBAL_GUEST_PERMISSION,
            'call_system_method': self.PermissionKeys.GLOBAL_SYSTEM_PERMISSION,
        }

    @property
    def validators(self) -> dict:
        return {
            'echo_validated': js.Object(
                {'data': js.Boolean(), 't': js.Number()}, required=['data'], additionalProperties=False
            ),
            'echo_custom_validated': self._validate,
        }

    @staticmethod
    async def guest() -> bool:
        return True

    async def store(self, data):
        self.stored = data

    @staticmethod
    async def echo(data=None, t: float = 0):
        await asyncio.sleep(t)
        return data

    @staticmethod
    async def fail():
        raise RuntimeError('Destined to fail!')

    async def retry(self, n: int = 0):
        self.retry_counter += 1
        if self.retry_counter >= n:
            self.retry_counter = 0
            return True
        raise TimeoutError('Needs retry!')

    async def echo_validated(self, data: bool, t: float = 0):
        return await self.echo(data, t)

    @staticmethod
    def _validate(params: dict) -> dict:
        if params['data'] is not True:
            raise ValidationError
        return params

    async def echo_custom_validated(self, data: bool, t: float = 0):
        return await self.echo(data, t)

    async def echo_user(self):
        await asyncio.sleep(0)
        return self.get_user_id()

    async def echo_session(self):
        await asyncio.sleep(0)
        return self.get_session().id

    async def write_session(self, data):
        await asyncio.sleep(0)
        session = self.get_session()
        session.update(data)

    @staticmethod
    async def call_system_method():
        await asyncio.sleep(0)
        return True


@pytest.fixture
def mock_service(app) -> _MockService:
    service = _MockService(app=app)
    app.services.add_service(service)
    return service


class _MockListener(Listener):
    class MockTransport(Service):
        def __init__(self, *args, **kws):
            super().__init__(*args, **kws)
            self.stream = asyncio.LifoQueue()

        async def add(self, body, headers):
            await self.stream.put((body, headers))

    _transport: MockTransport

    async def close(self):
        await self._transport.stream.join()
        await super().close()

    @classmethod
    def get_transport_cls(cls) -> Type:
        return _MockListener.MockTransport

    async def _read_batch(self) -> list:
        msg = await self._transport.stream.get()
        return [msg]

    async def _process_batch(self, batch: list) -> None:
        for msg in batch:
            await self._process_request(msg)
            self._transport.stream.task_done()


@pytest.fixture
def mock_listener(app, rpc, scheduler, mock_locks, mock_auth) -> _MockListener:
    transport = _MockListener.MockTransport(app)
    service = _MockListener(
        app=app,
        topic='test',
        transport=transport,
        authentication_service=mock_auth,
        rpc_service=rpc,
        scheduler=scheduler,
        locks_service=mock_locks,
    )
    app.services.add_service(transport)
    app.services.add_service(service)
    return service


class _MockStreamClient(StreamRPCClient):
    _transport: _MockListener.MockTransport

    @classmethod
    def get_transport_cls(cls) -> Type:
        return _MockListener.MockTransport

    async def write(self, body, headers: dict = None, key=None) -> None:
        if isinstance(body, list):
            body = [req.repr() for req in body]
        else:
            body = body.repr()
        await self._transport.stream.put((body, headers))


@pytest.fixture
def mock_stream_client(app, mock_listener, mock_users) -> _MockStreamClient:
    service = _MockStreamClient(
        app=app,
        app_name=app.name,
        topic='test',
        transport=mock_listener._transport,  # noqa
        auth_str=f'Basic {mock_users.username}:{mock_users.password}',
        request_logs=True,
        response_logs=True,
    )
    app.services.add_service(service)
    return service
