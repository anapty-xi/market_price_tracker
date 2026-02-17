from sqlalchemy import select

from .db.tables import Product, User
from .db import engine

class BaseInfrastructure:
    async def is_user_exists(self, tg_id: str) -> bool:
        '''
        Возвращает True если юзер существует, иначе False
        '''
        async with engine.async_session() as session:
            user = await session.execute(select(User).where(User.tg_id == tg_id))
            return user.scalar() is not None
        
    async def get_tracking_list(self, tg_id: str) -> list[str]:
        '''
        Получает список продуктов юзера, возвращает его в виде списка url. Если продукты отсутствуют возвращает пустой список
        '''
        async with engine.async_session() as session:
            tracking_list = await session.execute(select(Product).where(Product.user_id == tg_id))
            product_urls = [product.url for product in tracking_list.scalars().all()]
            return product_urls
        
