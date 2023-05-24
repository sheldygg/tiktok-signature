import asyncio
import os

from aiohttp.web import Application, AppRunner, TCPSite, json_response
from aiohttp.web_request import Request

from tiktok_signature.signature import Signer


async def get_request(request: Request):
    return json_response({"ok": True, "ip": request.remote})


async def post_request(request: Request):
    signer: Signer = request.app["signer"]
    post_data = await request.post()
    url = post_data.get("url")
    return json_response(await signer.sign(str(url)))


async def make_server(playwright, host: str, port: int):
    signer = Signer(playwright=playwright)
    await signer.init()
    app = Application()
    app["signer"] = signer
    app.router.add_post(path="/signature", handler=post_request)
    app.router.add_get(path="", handler=get_request)
    runner = AppRunner(app)
    await runner.setup()
    site = TCPSite(runner, host=host, port=port)
    return site


async def start_server(playwright, host: str, port: int):
    async with playwright() as pl:
        server = await make_server(playwright=pl, host=host, port=port)
        await server.start()
        await asyncio.Event().wait()


if __name__ == "__main__":
    from playwright.async_api import async_playwright

    asyncio.run(
        start_server(
            playwright=async_playwright,
            host=os.getenv("host", "127.0.0.1"),
            port=int(os.getenv("port", 8002)),
        )
    )
