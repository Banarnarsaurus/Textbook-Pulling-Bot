import aiohttp
from bs4 import BeautifulSoup

from typing import Iterable


class FreeLibrary:
    domain = None

    def __init__(self, client: aiohttp.ClientSession):
        self._client = client
        self.headers = None
        self.url = 'https://usa1lib.org/s/'

    def keywords_search_words(self, user_message):
        words = user_message.split()[1:]
        keywords = '%20'.join(words)
        search_words = ' '.join(words)
        return keywords, search_words

    async def search(self, keywords):
        async with self._client.get(self.url + keywords, headers=self.headers) as response:
            content = await response.content.read()
            soup = BeautifulSoup(content, 'html.parser')
            result_links = soup.findAll('a')
            return result_links

    def send_link(self, result_links: Iterable, search_words):
        send_link = set()
        for link in result_links:
            text = link.text.lower()
            if search_words in text:
                send_link.add(link.get('href'))
        return send_link
