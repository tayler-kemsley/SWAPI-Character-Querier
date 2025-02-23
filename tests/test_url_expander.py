import pytest
from aioresponses import aioresponses

from src.app import SWAPI


pytest_plugins = ('pytest_asyncio',)


async def add_responses(mock):
    for i in range(0, 5):
        mock.get(f'https://www.test.com/{i}', payload=dict(test=i))


@pytest.mark.asyncio
async def test_url_expander():
    with aioresponses() as mock:
        await add_responses(mock)
        res = await SWAPI().expand_urls({
            'name': 'Testing',
            'foo': 'https://www.test.com/1',
            'bar': [
                'https://www.test.com/2',
                'https://www.test.com/3'
            ]
        })
        assert res == {
            'name': 'Testing',
            'bar': [
                {'test': 2},
                {'test': 3}
            ],
            'foo': {'test': 1},
        }
