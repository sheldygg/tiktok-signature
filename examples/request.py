from httpx import AsyncClient


async def make_request(url: str, headers: dict):
    async with AsyncClient() as client:
        return await client.get(url=url, headers=headers)
