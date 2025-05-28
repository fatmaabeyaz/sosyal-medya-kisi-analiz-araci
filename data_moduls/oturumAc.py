import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # Twitter'a git
        page = await context.new_page()
        await page.goto("https://twitter.com/login")

        print("Lütfen manuel olarak giriş yapın...")
        await page.wait_for_timeout(10000)  # 60 saniye bekle (giriş yapman için)

        # Oturum bilgilerini kaydet
        cookie_path = os.path.join(os.path.dirname(__file__), "xCookie.json")
        await context.storage_state(path=cookie_path)
        print("Oturum bilgisi kaydedildi.")

        await browser.close()

asyncio.run(main())
