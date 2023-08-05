"""Shared cache services and classes."""

import abc
from typing import Collection, FrozenSet, List, Dict, Any, Optional, Type

from kaiju_tools.app import ContextableService, Service
from kaiju_tools.encoding import MimeTypes, serializers
from kaiju_tools.interfaces import Cache
from kaiju_tools.functions import RETRY_EXCEPTION_CLASSES
from kaiju_tools.types import NSKey

__all__ = ['BaseCacheService', 'Cache']


class BaseCacheService(ContextableService, Cache, abc.ABC):
    """Base class for shared cache."""

    service_name = 'cache'
    CONNECTION_ERROR_CLASSES = RETRY_EXCEPTION_CLASSES
    DEFAULT_SERIALIZER_TYPE = MimeTypes.msgpack

    def __init__(
        self,
        *args,
        transport: Service = None,
        serializer_type: Optional[str] = DEFAULT_SERIALIZER_TYPE,
        encoders=serializers,
        shared: bool = False,
        **kws,
    ):
        """Initialize.

        :param transport: transport service (Redis, DB or similar)
        :param serializer_type: you may specify a serializer type from `kaiju-tools.encoding`
        :param encoders: serializers registry with all serializers classes
        :param shared: use a shared namespace (i.e. between multiple apps)
        """
        super().__init__(*args, **kws)
        self.namespace = self.app.namespace_shared if shared else self.app.namespace
        self.namespace = self.namespace / '_cache'
        self._transport_name = transport
        self._serializer = encoders[serializer_type]() if serializer_type else None
        self._transport = None
        self._queue = None

    async def init(self):
        """Service context init."""
        self._transport = self.discover_service(self._transport_name, cls=self.get_transport_cls())

    @classmethod
    @abc.abstractmethod
    def get_transport_cls(cls) -> Type:
        """Get transport class required for this service."""

    @abc.abstractmethod
    async def exists(self, id: NSKey) -> bool:
        """Check if key is present in the cache."""

    @abc.abstractmethod
    async def m_exists(self, id: Collection[NSKey]) -> FrozenSet[str]:
        """Return a set of existing keys."""

    async def get(self, id: NSKey):
        """Get value of a key or None if not found."""
        self.logger.debug('get', key=id)
        value = await self._get(id)
        value = self._load_value(value)
        return value

    @abc.abstractmethod
    async def _get(self, key: NSKey):
        """Return a key value or None if not found."""

    async def m_get(self, id: Collection[NSKey]) -> Dict[NSKey, Any]:
        """Get values of multiple keys."""
        self.logger.debug('m_get', keys=id)
        values = await self._m_get(*id)
        if values:
            return {k: self._load_value(v) for k, v in zip(id, values) if v}  # noqa
        return {}

    @abc.abstractmethod
    async def _m_get(self, *keys: NSKey) -> List[NSKey]:
        """Return a list of values for given keys."""

    async def set(self, id: NSKey, value: Any, ttl: int = None) -> None:
        """Set a single key."""
        self.logger.info('set', key=id)
        value = self._dump_value(value)
        await self._set(id, value, ttl)

    @abc.abstractmethod
    async def _set(self, key: NSKey, value: bytes, ttl: Optional[int]):
        """Set a key value with ttl in sec (0 for infinite)."""

    async def m_set(self, data: Dict[NSKey, Any], ttl: int = None) -> None:
        """Set multiple keys."""
        key_dict = {k: self._dump_value(v) for k, v in data.items()}
        self.logger.info('m_set', keys=data.keys(), ttl=ttl)
        await self._m_set(key_dict, ttl)

    @abc.abstractmethod
    async def _m_set(self, keys: Dict[NSKey, bytes], ttl: int):
        """Set multiple keys at once with ttl in sec (0 for inf)."""

    async def delete(self, id: NSKey) -> None:
        """Remove a key from cache."""
        self.logger.info('delete', key=id)
        await self._delete(id)

    @abc.abstractmethod
    async def _delete(self, key: str):
        """Remove one key at once."""

    async def m_delete(self, id: Collection[NSKey]) -> None:
        """Remove multiple keys at once."""
        self.logger.info('m_delete', keys=id)
        await self._m_delete(*id)

    @abc.abstractmethod
    async def _m_delete(self, *keys: NSKey):
        """Remove multiple keys at once."""

    def _load_value(self, value):
        if value is None:
            return
        elif self._serializer:
            return self._serializer.loads(value)
        else:
            return value

    def _dump_value(self, value):
        if self._serializer:
            return self._serializer.dumps(value)
        else:
            return value
