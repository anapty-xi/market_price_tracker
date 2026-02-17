from decimal import Decimal
from datetime import date
from sqlalchemy import select, insert

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
        pass



