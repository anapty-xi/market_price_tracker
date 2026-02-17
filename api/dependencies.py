from typing import Annotated
from fastapi import Header

from usecases.user import user_usecases
from usecases.product import product_usecases
from infrastructure import user_infrastructure, product_infrastructure

def user_tg_id(x_telegram_id: Annotated[str, Header()]) -> str:
    return x_telegram_id



'''заивисимости для users_routs (pl - products list)'''

def get_pl_usecase() -> user_usecases.GetProductList:
    return user_usecases.GetProductList(user_infrastructure.UserDbGateway)

def pl_operations_usecase() -> user_usecases.ProductListOperations:
    return user_usecases.ProductListOperations(user_infrastructure.UserDbGateway)


'''зависимости для products_routs'''

def parse_product_data_usecase() -> product_usecases.ParseProductsData:
    return product_usecases.ParseProductsData(db_infrastructure=product_infrastructure.ProductDBGateway,
                                              parser_infrastructure=product_infrastructure.ProductParser)

def get_products_price_track() -> product_usecases.GetProductPriceTrack:
    return product_usecases.GetProductPriceTrack(db_infrastructure=product_infrastructure.ProductDBGateway)

def parse_all_products_for_db() -> product_usecases.ParseAllProductsForDB:
    return product_usecases.ParseAllProductsForDB(db_infrastructure=product_infrastructure.ProductDBGateway,
                                                  parser_infrastructure=product_infrastructure.ProductParser)