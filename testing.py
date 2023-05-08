from time import perf_counter
import aiohttp
import asyncio

async def fetch(s, id):
    async with s.get(f'https://hacker-news.firebaseio.com/v0/item/{id}.json?print=pretty') as r:
        if r.status != 200:
            r.raise_for_status()
        return await r.text()

async def fetch_all(s, ids):
    tasks = []
    for id in ids:
        task = asyncio.create_task(fetch(s, id))
        tasks.append(task)
    res = await asyncio.gather(*tasks)
    return res

async def main():
    ids = [35863837] #, 35865678, 35864429, 35864661, 35863309, 35862837, 35861435, 35864484, 35862142, 35865010, 35865855, 35864053, 35865257, 35859338, 35852710]
    async with aiohttp.ClientSession() as session:
        htmls = await fetch_all(session, ids)
        print(htmls)

if __name__ == '__main__':
    start = perf_counter()
    asyncio.run(main())
    stop = perf_counter()
    print("time taken:", stop - start)
    # time taken: 14.692326207994483