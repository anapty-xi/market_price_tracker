from sqlalchemy import delete, and_, select
from sqlalchemy.dialects.postgresql import insert

from usecases.user.user_protocol import UserProtocol
from .db.tables import Product, User
from .db import engine

class UserDbGateway(UserProtocol):
    async def delete_product(self, tg_id: str, product_url: str) -> bool:
        '''
        Удалаяет продукт из списка продуктов юзера и возвращает True. Если удаление не удалось возвращает False
        '''
        async with engine.async_session() as session:
            async with session.begin():
                resurl = await session.execute(delete(Product).where(
                    and_(Product.user_id == tg_id, Product.url == product_url) 
                    ).returning(Product))
                
                return resurl.scalar() is not None
    
    async def add_product(self, tg_id: str, product_url: str) -> bool:
        '''
        Добавляет продукт в список продуктов юзера и возвращает True. Если добавление не удалось возвращает False
        '''
        async with engine.async_session() as session:
            async with session.begin():
                result = await session.execute(insert(Product).values(url = product_url, user_id = tg_id).returning(Product))
                return result.scalar() is not None

    async def get_tracking_list(self, tg_id: str) -> list[str]:
        '''
        Получает список продуктов юзера, возвращает его в виде списка url. Если продукты отсутствуют возвращает пустой список
        '''
        async with engine.async_session() as session:
            tracking_list = await session.execute(select(Product).where(Product.user_id == tg_id))
            product_urls = [product.url for product in tracking_list.scalars().all()]
            return product_urls


        
    async def is_user_exists(self, tg_id: str) -> bool:
        '''
        Возвращает True если юзер существует, иначе False
        '''
        async with engine.async_session() as session:
            user = await session.execute(select(User).where(User.tg_id == tg_id))
            return user.scalar() is not None


    async def create_if_not_exists(self, tg_id: str) -> None:
        '''
        Создает юзера если он не существует
        '''
        async with engine.async_session() as session:
            async with session.begin():
                await session.execute(insert(User).values(tg_id=tg_id).on_conflict_do_nothing())