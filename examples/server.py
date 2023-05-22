import asyncio

from playwright.async_api import async_playwright
from pydantic import BaseSettings
from tiktok_signature.server import make_server


class Settings(BaseSettings):
    host: str
    port: int

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


async def main():
    playwright = await async_playwright().start()
    settings = Settings()
    try:
        server = await make_server(playwright=playwright, host=settings.host, port=settings.port)
        await server.start()
        await asyncio.Event().wait()
    finally:
        await playwright.stop()

asyncio.run(main())
