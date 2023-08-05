"""Message stream services and classes."""

import abc
import asyncio
from typing import Union, List, Type, final

from kaiju_tools.app import ContextableService, Scheduler, Service
from kaiju_tools.interfaces import Locks, SessionInterface, AuthenticationInterface
from kaiju_tools.rpc import RPCRequest, RPCError, JSONRPCServer, BaseRPCClient
from kaiju_tools.types import Namespace
from kaiju_tools.logging import Adapter
from kaiju_tools.encoding import MimeTypes, serializers

__all__ = ['Listener', 'StreamRPCClient', 'Topic']


@final
class Topic:
    """Default topic names."""

    RPC = 'rpc'
    MANAGER = 'manager'
    EXECUTOR = 'executor'


class Listener(ContextableService, abc.ABC):
    """Stream consumer assigned to a particular topic."""

    content_type = MimeTypes.msgpack
    lock_check_interval = 1

    def __init__(
        self,
        app,
        topic: str,
        rpc_service: JSONRPCServer = None,
        locks_service: Locks = None,
        scheduler: Scheduler = None,
        session_service: SessionInterface = None,
        authentication_service: AuthenticationInterface = None,
        transport: Service = None,
        shared: bool = False,
        max_parallel_batches: int = None,
        logger: Adapter = None,
    ):
        super().__init__(app=app, logger=logger)
        self._transport = transport
        self.topic = topic
        self.max_parallel_batches = max_parallel_batches
        self._counter = asyncio.Semaphore(max_parallel_batches) if max_parallel_batches else None
        _ns = self.app.namespace_shared if shared else self.app.namespace
        _ns = _ns / '_stream'
        self._key = _ns.get_key(self.topic)
        self._lock_key = _ns.create_namespace('_lock').get_key(self.topic)
        self._lock_id = None
        self._scheduler = scheduler
        self._rpc = rpc_service
        self._locks = locks_service
        self._sessions = session_service
        self._auth = authentication_service
        self._unlocked = asyncio.Event()
        self._idle = asyncio.Event()
        self._loop = None
        self._lock_task = None
        self._closing = True
        self._encoder = serializers[self.content_type]()

    async def init(self):
        self._closing = False
        self._unlocked.set()
        self._idle.set()
        self._rpc = self.discover_service(self._rpc, cls=JSONRPCServer)
        self._locks = self.discover_service(self._locks, cls=Locks)
        self._sessions = self.discover_service(self._sessions, cls=SessionInterface, required=False)
        self._transport = self.discover_service(self._transport, cls=self.get_transport_cls())
        self._scheduler = self.discover_service(self._scheduler, cls=Scheduler)
        self._auth = self.discover_service(self._auth, cls=AuthenticationInterface, required=False)
        self._loop = asyncio.create_task(self._read(), name=f'{self.service_name}.{self.topic}._read')
        self._lock_task = self._scheduler.schedule_task(
            self._check_lock, interval=self.lock_check_interval, name=f'{self.service_name}._check_lock'
        )

    async def close(self):
        self._closing = True
        self._lock_task.enabled = False
        await self._idle.wait()

    @classmethod
    @abc.abstractmethod
    def get_transport_cls(cls) -> Type:
        ...

    async def lock(self) -> None:
        self.logger.info('lock', topic=self._key)
        self._lock_id = await self._locks.acquire(self._lock_key)
        self._unlocked.clear()
        await asyncio.sleep(self.lock_check_interval)  # ensure that everyone else is locked
        if not self._idle.is_set():
            await self._idle.wait()

    async def unlock(self) -> None:
        self.logger.info('unlock', topic=self._key)
        if self._lock_id:
            await self._locks.release(self._lock_key, self._lock_id)
            self._lock_id = None
        self._unlocked.set()

    @property
    def locked(self) -> bool:
        return not self._unlocked.is_set()

    @abc.abstractmethod
    async def _read_batch(self) -> list:
        """Get messages from a stream."""

    @abc.abstractmethod
    async def _process_batch(self, batch: list) -> None:
        """Define your own message processing and commit here."""

    async def _process_request(self, data) -> None:
        """Process a single request in a batch."""
        body, headers = data
        headers, result = await self._rpc.call(body=body, headers=headers, nowait=True)
        if type(result) is RPCError:  # here it can be only a pre-request error due to nowait=False
            self.logger.info('Client error', result=result)

    async def _read(self) -> None:
        """Read from a stream."""
        self.logger.info('Starting')
        while not self._closing:
            await self._unlocked.wait()
            try:
                batch = await self._read_batch()
                self._idle.clear()
                if self.max_parallel_batches:
                    async with self._counter.acquire():
                        if batch:
                            await self._process_batch(batch)
                else:
                    if batch:
                        await self._process_batch(batch)
            except Exception as exc:
                self.logger.error('Read error', exc_info=exc, topic=self._key)
            finally:
                self._idle.set()

    async def _check_lock(self) -> None:
        """Check for existing shared lock and lock / unlock if needed."""
        existing = await self._locks.m_exists([self._lock_key])
        if self._lock_key in existing:
            if not self.locked:
                self._unlocked.clear()
        elif self.locked:
            self._unlocked.set()


class StreamRPCClient(BaseRPCClient, abc.ABC):
    """Stream client for RPC requests."""

    transport_cls: Type

    def __init__(self, *args, app_name: str, topic: str = Topic.RPC, shared: bool = False, **kws):
        """Initialize.

        :param app_name: application (topic) name
        :param listener_service: stream listener service instance
        :param topic: topic name
        """
        super().__init__(*args, **kws)
        if shared:
            app_name = '__shared__'
        self._topic = Namespace(env=self.app.env, name=app_name).create_namespace('_stream').get_key(topic)

    async def init(self):
        self._transport = self.discover_service(self._transport, cls=self.get_transport_cls())
        await super().init()

    @classmethod
    @abc.abstractmethod
    def get_transport_cls(cls) -> Type:
        """Get transport class required for this service."""

    @abc.abstractmethod
    async def write(self, body, headers: dict = None, key=None) -> None:
        """Submit a message to a stream.

        :param body: message body
        :param headers: message headers
        :param key: (optional) unique message id
        """

    async def _request(self, body: Union[RPCRequest, List[RPCRequest]], headers: dict) -> None:
        """Send an RPC request via stream."""
        if type(body) is list:  # automatically make them notify because stream is a one-way interaction
            for row in body:
                row.id = None
        else:
            body.id = None
        await self.write(body, headers=headers)
