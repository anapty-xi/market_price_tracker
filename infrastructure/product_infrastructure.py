import asyncio
import random
from decimal import Decimal
from datetime import date
from sqlalchemy import select, insert
from playwright_stealth import Stealth
from playwright.async_api import async_playwright
from loguru import logger

from usecases.product.product_protocol import ProductDBProtocol, ProductParserProtocol
from .base_infrastructure import BaseInfrastructure
from .db import engine
from .db.tables import PriceHistory



async def main():
    with Stealth().use_async(async_playwright()) as p:

        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                                            viewport = {'width': 1920, 'height': 1080})

        page = await context.new_page()
        await page.goto("https://market.yandex.ru/card/uniqlo-x-jw-anderson-jw-anderson-collaboration-fw25-sweater-unisex-44-46/4730198529?do-waremd5=sg1Px_fxLwDEd_-N-gjnpw&cpc=qf0cGfEJ0NNs_OfgvEE-YpoMKEkhTTUOJG_5WmfPPE3hKj4t392qzIpPHJ34kku3NxE7sf0GIW3AIxMt1nL3SvoCHzNmidQX_1KT34sFDcmyEnpOBtbwmKw-LsxqKzwwhIHJOWZx_DI97v6p-a77fJXqa4H7wUQUd6x2W0j9qBsaznVJnQmdexeNSVkg62CI46z84fsTk8vpI_vkFbiXEzQTB61-kaRTVIlxf2iFK-qfrn-wWgjwK2ToWSMgRWhxpohOVFwzMLQXbqWl63oVBG8pOuAuTdAMeqpmHaDjtqU4LyLvUdzXXkaDZPTEQ8fHI84w-5lpkFUeuBTQYyj1OaoqiRNo4werAyJLpJdjN0ebGUDRReMVjpkpiiLJKeaUJESFxoITnWO-ZKhmUM6p644BMbWK5BxpsjXtIXWQyoWj7_CMiK2WjKLd2k8gCQF_J1KO1zDR02xV59qMJR1Vojny1OQGZGQXKvd5mhQP_GI%2C&ultima=1&ogV=-12")

        await asyncio.sleep(random.randint(1, 3))
        await page.mouse.wheel(500, 0)
        await asyncio.sleep(random.randint(2, 3))
        price = await page.locator('[data-auto="snippet-price-current"]').inner_text()
        print(price)
        await browser.close()

asyncio.run(main())

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
        parse_tasks = [asyncio.create_task(self._parse_proccess(product_url)) for product_url in products_urls]
        done, pending = await asyncio.wait(parse_tasks, return_when=asyncio.FIRST_EXCEPTION)
        for task in done:
            if task.exception():
                logger.error(f"Ошибка парсинга на первой попытке: {task.exception()}")
            else:
                products_data.append(task.result())
        if pending:
            for i in range(3):
                asyncio.sleep(3)
                done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_EXCEPTION)
                for task in done:
                    if task.exception():
                        logger.error(f"Ошибка парсинга ошибка парсинга на {i+2} попытке: {task.exception()}")
                    else:
                        products_data.append(task.result())
            if pending:
                for task in pending:
                    logger.error(f"Ошибка парсинга: {task.exception()} последущих попыток не будет")
                    task.cancel()
        return products_data



    async def _parse_proccess(product_url: str) -> dict[str, str | Decimal | bool]:
        async with Stealth().use_async(async_playwright()) as p:

            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                                                viewport = {'width': 1920, 'height': 1080})

            page = await context.new_page()
            await page.goto("https://market.yandex.ru/card/remen-chernim-cherno-molniya-serebryanyy/103320524950?do-waremd5=7guan-73hkpmBt1nWQQiEw&sponsored=1&cpc=Sd6dakNBfdwI2kafe_U0Eiw23r22MjCdX4WTDtXOx-SsbdtEOAqRrbRQ8BxBWLOyP3ay7xr6LZq9GSZnYfBu_bDctGPsqAGtYgyHiLoeWxfe_X-jvCv3cPwby9_M3QoALZ7PkReJ8aAyxBg2JobzMLeuOmJAcnVEFgM9cvfB7kgTssQYiVymF1A13KXz9k5MHM71hDIgfFoiaCcKC1x1PLM6nss5D6A-tHi6pS0m_QBZBJdTv4rM-txyt9rDwYLJ5FR-dTU4z9pLPiWKAni-Uft0Lw2_e8eEFjJJ5F3k91Wj5E9QDAzHLdDmhOkjG-xHBcCVH2MQB35lQ_wuUXMKgUjuHJinpCEYVoQiAINPj0lVinB2Y2OtaV0Ytet7nMwhyLPlh_OEEiidPbRZbfxW8YB09Wok2U7FjESa-E5DU2fIntP7ZGUj5dZYKNeCPJyttsyoocqQHwODgr4bTcxwCq81m3aW96yy42JYn8DIudkB7WdYRIRIawULjH3X-wKHCSvh5fHSfxiP8v_g799xMErzT5ECvuFUTa9Yqbdrk1c%2C&ultima=1&ogV=-12")

            await asyncio.sleep(random.randint(1, 3))
            await page.mouse.wheel(0, 0)
            await asyncio.sleep(random.randint(2, 3))

            card_info_container = page.locator('[id="cardAddButton"]')
            price = await card_info_container.locator('[data-auto="snippet-price-current"]').first.inner_text()
            title = await page.locator('[id="/content/page/fancyPage/defaultPage/productTitle"]').inner_text()
            await browser.close()

            pretty_price = Decimal(''.join(price.split()[:-1]))
            pretty_name = ' '.join(title.split())
            
            return {'name': pretty_name, 'price': pretty_price, 'is_active': True, 'product_url': product_url}

