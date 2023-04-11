import argparse
import asyncio

import aiohttp

URL = 'https://picsum.photos/400/400'


async def get_image(idx):
    async with aiohttp.ClientSession() as session:
        response = await session.get(URL)
        img_bytes = await response.read()
        with open(f'artifacts/easy/image_{idx}.jpg', 'wb') as f:
            f.write(img_bytes)


async def start(n):
    tasks = [asyncio.create_task(get_image(idx)) for idx in range(n)]
    results = await asyncio.gather(*tasks)
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", default=10, type=int)

    args = parser.parse_args()
    asyncio.run(start(n=args.number))
