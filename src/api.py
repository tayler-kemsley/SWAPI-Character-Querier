import aiohttp
import requests

from aiohttp import ClientSession
from typing import Optional
from urllib.parse import urlparse

from exceptions import NotFound


class SWAPI:
    base_url = "https://swapi.dev/api"

    def __init__(self):
        self.character_name: Optional[str] = None
        self.data: Optional[dict] = None

    async def search(self, type_name: str, query: str) -> dict:
        """
        Run a search query against the SW API
        """
        resp = requests.get(f'{self.base_url}/{type_name}/?search={query}')
        resp.raise_for_status()
        results: list[dict] = resp.json()['results']
        if not results:
            raise NotFound()
        # Expand urls
        self.character_name = results[0]['name']
        self.data = await self.expand_urls(results[0])
        return self.data

    async def is_url(self, url_str: str) -> bool:
        """
        Determine if a string is a URL
        """
        try:
            parsed = urlparse(url_str)
            return all([parsed.scheme, parsed.netloc])
        except AttributeError:
            return False

    async def async_get(self, session: ClientSession, url: str) -> dict:
        """
        Run Async get query
        """
        async with session.get(url) as response:
            return await response.json()

    async def expand_urls(self, data: dict) -> dict:
        """
        Given a response from the SW API, expand all the URLs in the response
        async
        Return the original dict with the URLs replaced with the response
        """
        async with aiohttp.ClientSession() as session:
            for k, v in data.items():
                if isinstance(v, list):
                    expanded_data = []
                    for val in v:
                        if await self.is_url(val):
                            expanded_data.append(
                                await self.async_get(session, val)
                            )
                    if expanded_data:
                        data[k] = expanded_data
                else:
                    if await self.is_url(v):
                        expanded_data = await self.async_get(session, v)
                        data[k] = expanded_data
        self.data = data
        return data
