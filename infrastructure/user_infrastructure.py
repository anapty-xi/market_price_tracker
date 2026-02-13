from sqlalchemy.orm import selectinload
from sqlalchemy import delete, and_, select

from usecases.user.user_protocol import UserProtocol
from .db.tables import Product
from .db.engine import async_session

class UserDbGateway(UserProtocol):
    async def delete_product(self, tg_id: str, product_url: str) -> None:
        async with async_session() as session:
            async with session.begin():
                await session.execute(delete(Product).where(
                    and_(Product.user_id == tg_id, Product.url == product_url) 
                    ))
        
    async def add_product(self, tg_id: str, product_url: str) -> None:
        async with async_session() as session:
            async with session.begin():
                product = Product(url=product_url, user_id=tg_id)
                session.add(product)

    async def get_tracking_list(self, tg_id: str) -> list[str]:
        async with async_session() as session:
            tracking_list = await session.execute(select(Product.url).where(Product.user_id == tg_id)).scalars().all()
            return tracking_list