from usecases.user.user_protocol import UserProtocol
from entities.user import User

class BaseUsecase:
    def __init__(self, infrastructure: UserProtocol):
        self.infrastructure = infrastructure()


class ProductListOperations(BaseUsecase):
    async def execute(self, tg_id: str, product_url: str, delete: bool = False, add: bool = False) -> bool | Exception:
        if not delete and not add:
            raise ValueError('Either delete or add must be True')
        
        if delete:
            try:
                self.infrastructure.delete_product(tg_id, product_url)
                return True
            except Exception as e:
                return e
        
        if add:
            try:
                self.infrastructure.add_product(tg_id, product_url)
                return True
            except Exception as e:
                return e
            
class GetProductList(BaseUsecase):
    async def execute(self, tg_id: str) -> User | Exception:
        try:
            products_list = self.infrastructure.get_product_list(tg_id)
        except Exception as e:
            return e
        
        return User(tg_id=tg_id, tracking_list=products_list)

            
