import asyncio
import random
from decimal import Decimal
from datetime import date
from sqlalchemy import select, insert
from playwright_stealth import Stealth
from playwright.async_api import async_playwright, Browser
from loguru import logger

from usecases.product.product_protocol import ProductDBProtocol, ProductParserProtocol
from .base_infrastructure import BaseInfrastructure
from .db import engine
from .db.tables import PriceHistory

class ProductDBGateway(BaseInfrastructure, ProductDBProtocol):
    async def get_product_price_track(self, product_url: str) -> dict[date, Decimal]:
        async with engine.async_session() as session:
            track_data = await session.execute(select(PriceHistory).where(PriceHistory.product_url==product_url))
            if track_data.scalars().first():
                return {}
            return {row.date: row.price for row in track_data.scalars().all()}

    async def save_new_price_data(self, products_data: list[dict[str, str | Decimal | bool]]) -> bool:
        async with engine.async_session() as session:
            async with session.begin():
                result = await session.execute(insert(PriceHistory).returning(PriceHistory), products_data) 
                return result.scalars().first() is not None



class ProductParser(ProductParserProtocol):
    async def parse_products_data(self, products_urls: list[str]) -> list[dict[str, str | Decimal | bool]]:
        products_data = []

        async with Stealth().use_async(async_playwright()) as p:
            browser = await p.chromium.launch(headless=True)
            parse_tasks = [asyncio.create_task(self._parse_proccess(browser, product_url)) for product_url in products_urls]
            done, pending = await asyncio.wait(parse_tasks, return_when=asyncio.FIRST_EXCEPTION)

            for task in done:
                if task.exception():
                    logger.error(f"Ошибка парсинга на первой попытке: {task.exception()}")
                else:
                    products_data.append(task.result())

            if pending:
                for i in range(3):
                    await asyncio.sleep(3)
                    done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_EXCEPTION)
                    for task in done:
                        if task.exception():
                            logger.error(f"Ошибка парсинга ошибка парсинга на {i+2} попытке: {task.exception()}")
                        else:
                            products_data.append(task.result())
                    if not pending:
                        break

                if pending:
                    for task in pending:
                        logger.error(f"Ошибка парсинга: {task.exception()} последущих попыток не будет")
                        task.cancel()

            await browser.close()
            return products_data



    async def _parse_proccess(self, browser: Browser, product_url: str) -> dict[str, str | Decimal | bool]:
        context = await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                                            viewport = {'width': 1920, 'height': 1080})

        page = await context.new_page()
        await page.goto(product_url)

        await asyncio.sleep(random.randint(1, 3))
        await page.mouse.wheel(0, 0)
        await asyncio.sleep(random.randint(2, 3))

        card_info_container = page.locator('[id="cardAddButton"]')
        price = await card_info_container.locator('[data-auto="snippet-price-current"]').first.inner_text()
        logger.info(f'цена {product_url} успешно получена')
        title = await page.locator('[id="/content/page/fancyPage/defaultPage/productTitle"]').inner_text()
        logger.info(f'название {title} успешно получено')
        await page.close()

        pretty_price = Decimal(''.join(price.split()[:-1]))
        pretty_name = ' '.join(title.split())
        
        return {'name': pretty_name, 'price': pretty_price, 'url': product_url, 'available': True}

