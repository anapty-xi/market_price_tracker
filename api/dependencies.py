from typing import Annotated
from fastapi import Header

from usecases.user import user_usecases
from usecases.product import product_usecases
from infrastructure import user_infrastructure, product_infrastructure

def user_tg_id(x_telegram_id: Annotated[int, Header()]) -> int:
    return x_telegram_id



'''заивисимости для users_routs (pl - products list)'''

def get_pl_usecase() -> user_usecases.GetProductList:
    return user_usecases.GetProductList(user_infrastructure.UserDbGateway)

def pl_operations_usecase() -> user_usecases.ProductListOperations:
    return user_usecases.ProductListOperations(user_infrastructure.UserDbGateway)


'''зависимости для products_routs'''

def get_products_info_usecase() -> product_usecases.GetProductsInformation:
    return product_usecases.GetProductsInformation(product_infrastructure.ProductParser)

def product_price_changes_usecase() -> product_usecases.GetProductPriceChange:
    return product_usecases.GetProductPriceChange(product_infrastructure.ProductDBGateway)