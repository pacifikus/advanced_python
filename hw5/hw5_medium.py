import os
import asyncio
from bs4 import BeautifulSoup
import json
import aiohttp

BASE_URL = 'https://www.avito.ru'
URL = f'{BASE_URL}/krasnoyarsk/kvartiry/sdam/'
RESULT_PATH = 'artifacts/medium/result.json'


async def parse(session):
    async with session.get(URL) as response:
        html = await response.text()

    soup = BeautifulSoup(html, 'html.parser')
    result = []
    for item in soup.find_all(
            'div',
            {'class': lambda x: x and 'iva-item-body' in x},
    ):
        header = item.find('h3').text.strip()
        print(header)
        price = item.find(
            'span',
            {'class': lambda x: x and 'price-root' in x},
        ).text.strip()
        url = BASE_URL + item.find('a', href=True)['href']
        text = item.find(
            'div',
            {'class': lambda x: x and 'iva-item-descriptionStep' in x},
        ).text.strip()
        result.append(
            {'header': header, 'url': url, 'price': price, 'text': text}
        )
    return result


async def start():
    async with aiohttp.ClientSession() as session:
        result = await parse(session)

        data = []
        if os.path.exists(RESULT_PATH):
            with open(RESULT_PATH, 'r') as f:
                data = json.load(f)
        data.extend(result)
        with open('artifacts/medium/result.json', 'w', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

asyncio.run(start())
