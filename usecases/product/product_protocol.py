from typing import Protocol
from decimal import Decimal
from datetime import date

class ProductDBProtocol(Protocol):
    async def get_tracking_list(self, tg_id: str) -> list[str]:
        ...
    async def is_user_exist(self, tg_id: str) -> bool:
        ...
    async def get_product_price_track(self, product_url: str) -> dict[date, Decimal]:
        ...
    async def save_new_price_data(self, products_data: list[dict[str, str | Decimal | bool]]) -> bool:
        ...

class ProductParserProtocol(Protocol):
    async def parse_products_data(self, products_urls: list[str]) -> list[dict[str, str | Decimal | bool]]:
        ...
