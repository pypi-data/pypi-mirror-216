import uuid
from datetime import datetime
from time import time
from typing import Hashable, List

import pytest  # noqa: pycharm
import pytest_asyncio

from kaiju_tools.interfaces import DataStore

__all__ = ['TestDataStore']


@pytest.mark.asyncio
class TestDataStore:
    @pytest_asyncio.fixture
    async def _store(self, app, mock_data_store) -> DataStore:
        async with app.services:
            yield mock_data_store

    @pytest.fixture(params=['single_key', 'composite_key'])
    def _row(self, request, mock_data_store):
        def _wrapper() -> (Hashable, dict):
            _row = {
                'id': uuid.uuid4().hex,
                'uuid': uuid.uuid4(),
                'name': 'row',
                'value': 0,
                'enabled': True,
                'timestamp': int(time()),
                'created': datetime.now(),
            }
            if request.param == 'single_key':
                mock_data_store.primary_key = 'id'
                return _row['id'], _row
            elif request.param == 'composite_key':
                mock_data_store.primary_key = ('id', 'uuid')
                return (_row['id'], _row['uuid']), _row

        return _wrapper

    @pytest.fixture
    def _rows(self, _row):
        def _wrapper() -> (List[Hashable], List[dict]):
            rows = [_row() for _ in range(10)]
            row_id, data = [r[0] for r in rows], [r[1] for r in rows]
            for n, row in enumerate(data):
                row['name'] = f'{row["name"]}_{n}'
                row['value'] = n
            return row_id, data

        return _wrapper

    async def test_singular(self, _store, _row):
        row_id, data = _row()
        _data = await _store.create(data)
        assert _data == data
        exists = await _store.exists(row_id)
        assert exists
        await _store.update(row_id, {'enabled': False})
        _data = await _store.get(row_id)
        assert _data['enabled'] is False
        await _store.delete(row_id)
        exists = await _store.exists(row_id)
        assert not exists

    async def test_multi(self, _store, _rows):
        row_id, data = _rows()
        _data = await _store.m_create(data, columns=['id'])
        assert len(data) == len(row_id)
        exists = await _store.m_exists(row_id)
        assert set(exists) == set(row_id)
        await _store.m_update(row_id, {'enabled': False})
        _data = await _store.m_get(row_id)
        assert all(not _r['enabled'] for _r in _data)
        await _store.m_delete(row_id)
        exists = await _store.m_exists(row_id)
        assert not exists

    async def test_conditionals(self, _store, _rows):
        row_id, data = _rows()
        await _store.m_create(data)
        await _store.m_update([], {'enabled': False}, conditions={'enabled': True})
        _data = await _store.m_get(row_id)
        assert all(not _r['enabled'] for _r in _data)
        await _store.m_delete([], conditions={'enabled': False})
        exists = await _store.m_exists(row_id)
        assert not exists

    @pytest.mark.parametrize(
        'conditions, num_rows',
        [
            ({'enabled': True}, 10),
            ({'enabled': {'not': True}}, 0),
            ({'name': ['row_1', 'row_2', 'row_3']}, 3),
            ({'value': {'gt': 4, 'lt': 8}}, 3),
            ({'value': {'ge': 4, 'le': 8}}, 5),
            ({'name': {'like': 'row%'}}, 10),
        ],
        ids=['eq', 'not', 'in', 'compare', 'compare incl', 'like'],
    )
    async def test_conditions(self, _store, _rows, conditions, num_rows):
        row_id, data = _rows()
        await _store.m_create(data)
        counter = 0
        async for rows in _store.iter(limit=5, conditions=conditions):  # noqa ???
            counter += len(rows)
        assert counter == num_rows
