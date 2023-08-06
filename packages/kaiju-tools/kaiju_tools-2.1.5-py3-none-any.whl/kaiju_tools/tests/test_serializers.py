import datetime
import uuid
from typing import cast, Type

import pytest

from kaiju_tools.encoding import serializers, SerializerInterface, Serializable
from kaiju_tools.rpc import RPCRequest, RPCResponse, RPCError
from kaiju_tools.exceptions import InternalError


@pytest.fixture
def serializable_data():
    data = {
        'int': 42,
        'str': 'some text',
        'unicode': 'уникоде',
        'bool': True,
        'uuid': uuid.uuid4(),
        'list': ['some', 'text', 42],
        'time': datetime.datetime(2001, 1, 1, 1),
    }
    return data


@pytest.fixture
def serializable_special_objects():
    data = {
        'request': RPCRequest(id=1, method='test', params=None),
        'response': RPCResponse(id=1, result=[1, 2, 3]),
        'error': RPCError(id=None, error=InternalError('Internal error', base_exc=ValueError('Sht!'))),
    }
    return data


class _Serialized(Serializable):
    fields = None

    def __init__(self):
        self.a = 1
        self.b = None
        self._c = 2


@pytest.fixture(
    params=[
        {'fields': ['a', 'b'], '__slots__': None, 'serializable_attrs': None, 'include_null_values': True},
        {'fields': ['b'], '__slots__': ['b', '_c'], 'serializable_attrs': None, 'include_null_values': True},
        {'fields': ['b'], '__slots__': None, 'serializable_attrs': ['b'], 'include_null_values': True},
        {'fields': ['a'], '__slots__': None, 'serializable_attrs': None, 'include_null_values': False},
        {'fields': [], '__slots__': ['b', '_c'], 'serializable_attrs': None, 'include_null_values': False},
    ]
)
def _serialized(request):
    s = _Serialized
    for key, value in request.param.items():
        setattr(s, key, value)
    return s()


def test_serializable_objects(_serialized):
    serialized = _serialized.repr()
    assert list(serialized) == list(_serialized.fields)


@pytest.mark.parametrize('serializer', tuple(serializers.values()), ids=tuple(serializers.keys()))
def test_serializers(serializer, serializable_data, logger):
    serializer = cast(Type[SerializerInterface], serializer)()
    s = serializer.dumps(serializable_data)
    logger.debug(s)
    data = serializer.loads(s)
    logger.debug(serializable_data)
    logger.debug(data)
    assert serializable_data == data


@pytest.mark.parametrize('serializer', tuple(serializers.values()), ids=tuple(serializers.keys()))
def test_serializers_for_special_objects(serializer, serializable_special_objects, logger):
    serializer = cast(Type[SerializerInterface], serializer)()
    s = serializer.dumps(serializable_special_objects)
    logger.debug(s)
    data = serializer.loads(s)
    logger.debug(serializable_special_objects)
    logger.debug(data)
    assert {k: v.repr() for k, v in serializable_special_objects.items()} == data
