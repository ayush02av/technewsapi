from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import main
from typing import List
import requests
import asyncio
import aiohttp
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://hacker-news.firebaseio.com/v0/"
EXTRA = ".json?print=pretty"
LIMIT_PER_PAGE = 15

def get_url(endpoint):
    return BASE_URL + endpoint + EXTRA

async def fetch(session, id):
    async with session.get(get_url(f"item/{str(id)}")) as response:
        if response.status != 200:
            response.raise_for_status()
        return await response.json()

async def fetch_all(session, ids):
    tasks = []
    for id in ids:
        task = asyncio.create_task(fetch(session, id))
        tasks.append(task)
    res = await asyncio.gather(*tasks)
    return res

@app.get(
    "/{page}",
    response_model=List[main.GetNewsReponse]
)
async def get_news(page: int):
    try:
        response = requests.get(get_url('topstories'))

        start = (page - 1) * LIMIT_PER_PAGE
        
        news_ids = response.json()[start: start + LIMIT_PER_PAGE]

        async with aiohttp.ClientSession() as session:
            jsons = await fetch_all(session, news_ids)
        
        return jsons
        
    except Exception as exception:
        raise HTTPException(
            status_code = 500,
            detail = exception.__str__()
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)