# Tiktok Signature
****

**Server**

```python
python server.py
```

**As package**

```python
import asyncio

from tiktok_signature import Signer
from playwright.async_api import async_playwright

async def main():
    playwright = await async_playwright().start()
    try:
        signer = Signer(playwright=playwright)
        await signer.init()
        await signer.sign("url")
    finally:
        await playwright.stop()
        
asyncio.run(main())

```

**Docker**

Soon...