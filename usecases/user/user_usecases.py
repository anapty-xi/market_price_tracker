from usecases.user.user_protocol import UserProtocol
from entities.user import User
from entities.product import Product
from util.exeptions import UnexpectedDBExeption

class BaseUsecase:
    def __init__(self, infrastructure: UserProtocol):
        self.infrastructure = infrastructure()


class ProductListOperations(UserProtocol, BaseUsecase):
    async def execute(self, tg_id: str, product_url: str, delete: bool = False, add: bool = False) -> None | Exception:
        '''
        Позволяет удалять или добавлять продукты в список отслеживания пользователя. Требует один из аргументов (delete, add) в значении True, инче выкидывает ошибку.
        При удалении проверяет существет ли юзер и товар - если нет
        выкидывает ошибку. При добавлении проверяет существет ли юзер и нет ли такого же товара у юзера. Если юзера нет - создает его.
        Если товар уже был добавлен - выкидывает ошибку.
        '''
        if not delete and not add:
            raise ValueError('Either delete or add must be True')
        elif delete and add:
            raise ValueError('Only one of delete or add must be True')
        
        if delete:
            if await self.infrastructure.is_user_exists(tg_id):
                if not await self.infrastructure.delete_product(tg_id, product_url):
                    raise ValueError('Product does not exists')
            else:
                raise ValueError('User does not exists')

        
        if add:
            await self.infrastructure.create_if_not_exists(tg_id)
            if not await self.infrastructure.add_product(tg_id, product_url):
                raise UnexpectedDBExeption('Error ocured while adding product')
           

            
class GetProductList(UserProtocol, BaseUsecase):
    async def execute(self, tg_id: str) -> User | Exception:
        '''
        Возвращает сущность User с заполненным списком отслеживаемых товаров. Сущности Product в списке юзера имеют name, price, available = None
        Если юзера нет - выкидывает ошибку.
        '''
        if await self.infrastructure.is_user_exists(tg_id):
            products_list = await self.infrastructure.get_tracking_list(tg_id)
        else:
            raise ValueError('User does not exists')
        
        return User(tg_id=tg_id, tracking_list=[Product(name=None, price=None, url=product_url, available=None) for product_url in products_list])

            
