# Tiktok Signature

```pip install tiktok-signature```

**Server**

```python
import asyncio

from playwright.async_api import async_playwright
from pydantic import BaseSettings
from tiktok_signature.server import make_server


class Settings(BaseSettings):
    host: str
    port: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


async def main():
    settings = Settings()
    async with async_playwright() as playwright:
        server = await make_server(playwright=playwright, host=settings.host, port=settings.port)
        await server.start()
        await asyncio.Event().wait()

asyncio.run(main())

```

**As package**

```python
import asyncio

from tiktok_signature import Signer
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as playwright:
        signer = Signer(playwright=playwright)
        await signer.init()
        await signer.sign("url")
        
asyncio.run(main())

```

**Docker**

You can build image yourself
```
docker build . -t tiktok-signature
```
Or start immediately with the second command and use the ready image
```
docker run --name=tiktok-signature --restart=always -p 8002:8002 -e port=8002 sheldygg/tiktok-signature
```
