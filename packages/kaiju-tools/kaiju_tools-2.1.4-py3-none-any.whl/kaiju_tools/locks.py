"""Shared locks services and types."""

import abc
import asyncio
from time import time
from typing import Dict, Optional, List, FrozenSet, Type

from kaiju_tools.app import Service, ContextableService, Scheduler
from kaiju_tools.interfaces import Locks
from kaiju_tools.types import NSKey

__all__ = ['BaseLocksService', 'LockError', 'LockTimeout', 'NotLockOwnerError', 'LockExistsError', 'Scheduler', 'Locks']


class LockError(Exception):
    """Base class for lock related errors."""


class LockExistsError(LockError):
    """The same lock already exists."""


class NotLockOwnerError(LockError):
    """A lock can be released only by its owner."""


class LockTimeout(LockError, TimeoutError):
    """Timeout when trying to acquire a lock."""


class BaseLocksService(ContextableService, Locks, abc.ABC):
    """Base class for managing shared locks."""

    class ErrorCode:
        """Status and error codes for locks."""

        LOCK_EXISTS = 'LOCK_EXISTS'  #: the lock already present in the db
        NOT_LOCK_OWNER = 'NOT_OWNER'  #: service trying to release a lock is not a lock owner
        RUNTIME_ERROR = 'RUNTIME_ERROR'  #: any other error
        LOCK_ACQUIRE_TIMEOUT = 'LOCK_ACQUIRE_TIMEOUT'
        OK = 'OK'  #: OK

    service_name = 'locks'

    def __init__(
        self,
        *args,
        transport: Service = None,
        refresh_interval: int = 30,
        scheduler: str = None,
        shared: bool = False,
        **kws,
    ):
        """Initialize.

        :param transport: db / redis connector
        :param refresh_interval:  how often locks will be renewed
        :param shared: shared between apps
        """
        super().__init__(*args, **kws)
        self.namespace = self.app.namespace_shared if shared else self.app.namespace
        self.namespace = self.namespace / '_lock'
        self._transport_name = transport
        self._refresh_interval = max(1, int(refresh_interval))
        self._base_ttl = self._refresh_interval * 3
        self._scheduler = scheduler
        self._keys: Dict[NSKey, float] = {}
        self._closing = False
        self._transport = None
        self._task = None

    async def init(self):
        """Initialize."""
        self._transport = self.discover_service(self._transport_name, cls=self.get_transport_cls())
        self._scheduler = self.discover_service(self._scheduler, cls=Scheduler)
        self._closing = False
        self._task = self._scheduler.schedule_task(
            self._renew_keys,
            self._refresh_interval,
            name=f'{self.service_name}._renew_keys',
            policy=self._scheduler.ExecPolicy.CANCEL,
        )
        self._keys = {}

    async def close(self):
        """Close."""
        self._closing = True
        self._task.enabled = False

    @classmethod
    @abc.abstractmethod
    def get_transport_cls(cls) -> Type:
        """Get transport class required for this service."""

    async def acquire(
        self, id: NSKey, identifier: Locks.LockId = None, ttl: int = None, wait=True, timeout: float = None
    ) -> Locks.LockId:
        """Wait for lock and acquire it.

        :param id: lock name
        :param identifier: service/owner identifier, if id is None then the app['id'] will be used
        :param ttl: optional ttl in seconds, None for eternal (until app exists)
        :param wait: wait for a lock to release (if False then it will raise a `LockError`
            if lock with such key already exists)
        :param timeout: optional max wait time in seconds

        :raises LockExistsError:
        :raises LockAcquireTimeout: when timeout's reached
        :raises LockError: any internal error
        """
        if identifier is None:
            identifier = Locks.LockId(str(self.app.id))
        if ttl is None:
            raise ValueError('TTL must be set')

        t0 = time()

        while not self._closing:
            t = time()
            deadline = self._keys.get(id)
            if deadline and deadline > t:
                if not wait:
                    raise LockExistsError(id)
                elif timeout and t - t0 > timeout:
                    raise LockTimeout(id)
                await asyncio.sleep(1)
                continue

            actual_ttl = min(self._base_ttl, ttl)
            try:
                await self._acquire([id], identifier=identifier, ttl=actual_ttl)
            except LockExistsError:
                if not wait:
                    raise LockExistsError(id)
                elif timeout and t - t0 > timeout:
                    raise LockTimeout(id)
                await asyncio.sleep(1)
                continue

            self._keys[id] = time() + ttl
            self.logger.info('locked', key=id)
            return identifier

        raise LockTimeout(id)

    async def release(self, id: NSKey, identifier: Locks.LockId) -> None:
        """Release a lock.

        :param id: lock name
        :param identifier: service/owner identifier
        :raises LockError: if the lock can't be released by this service
        """
        self.logger.debug('release', key=id)
        try:
            await self._release([id], identifier)
        except NotLockOwnerError as exc:
            raise exc
        except Exception as exc:
            raise LockError(self.ErrorCode.RUNTIME_ERROR) from exc
        self.logger.info('released', key=id)
        if id in self._keys:
            del self._keys[id]

    async def owner(self, id: NSKey) -> Optional[Locks.LockId]:
        """Return a current lock owner identifier or None if not found / has no owner."""
        owner = await self._owner(id)
        return Locks.LockId(owner)

    async def is_owner(self, id: NSKey) -> bool:
        """Return `True` if the current instance is an owner of this lock."""
        owner = await self._owner(id)
        return str(owner) == str(self.app['id'])

    @abc.abstractmethod
    async def m_exists(self, id: List[NSKey]) -> FrozenSet[NSKey]:
        """Check if locks with such keys exist. Return a set of existing keys."""

    @abc.abstractmethod
    async def _acquire(self, keys: List[NSKey], identifier: Locks.LockId, ttl: int):
        """Set a list of specified keys. Also keep in mind that the operation must be atomic or transactional.

        :raises LockExistsError:
        """

    @abc.abstractmethod
    async def _release(self, keys: List[NSKey], identifier: Locks.LockId) -> None:
        """Release a lock.

        :raises NotALockOwnerError: provided identifier doesn't match with the stored value
        """

    @abc.abstractmethod
    async def _renew(self, keys: List[NSKey], values: List[int]) -> None:
        """Renew keys TTLs with the new provided values (in sec)."""

    @abc.abstractmethod
    async def _owner(self, key: NSKey) -> Locks.LockId:
        """Return a key owner or None if there's no key or owner."""

    async def _renew_keys(self):
        """Renew existing locks."""
        t = time()
        keys, values, to_remove = [], [], []

        for key, deadline in self._keys.items():
            if deadline is None:
                keys.append(key)
                values.append(self._refresh_interval)
            elif deadline <= t:
                to_remove.append(key)
            else:
                keys.append(key)
                ttl = min(deadline - t, self._refresh_interval)
                values.append(ttl)

        for key in to_remove:
            del self._keys[key]

        if keys:
            await self._renew(keys, values)
