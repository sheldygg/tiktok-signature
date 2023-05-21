import asyncio
import logging

from aiohttp.web import Application, AppRunner, TCPSite, json_response
from aiohttp.web_request import Request
from playwright.async_api import async_playwright

from tiktok_signature import Signer


async def get_request(request: Request):
    return json_response({"ok": True, "ip": request.remote})


async def post_request(request: Request):
    signer: Signer = request.app["signer"]
    post_data = await request.post()
    url = post_data.get("url")
    return json_response(await signer.sign(url))


logging.basicConfig(level=logging.INFO)


async def main():
    playwright = await async_playwright().start()
    try:
        signer = Signer(playwright=playwright)
        await signer.init()
        app = Application()
        app["signer"] = signer
        app.router.add_post(path="/signature", handler=post_request)
        app.router.add_get(path="", handler=get_request)
        runner = AppRunner(app)
        await runner.setup()
        site = TCPSite(runner, host="127.0.0.1", port=8002)
        await site.start()
        await asyncio.Event().wait()
    finally:
        await playwright.stop()


asyncio.run(main())
