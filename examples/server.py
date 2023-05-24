import asyncio

from playwright.async_api import async_playwright
from tiktok_signature.server import make_server


async def main():
    async with async_playwright() as playwright:
        server = await make_server(playwright=playwright, host="127.0.0.1", port=8002)
        await server.start()
        await asyncio.Event().wait()


asyncio.run(main())
