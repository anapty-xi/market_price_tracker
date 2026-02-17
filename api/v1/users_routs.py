from fastapi import APIRouter, HTTPException, status, Depends, Body
from typing import Annotated
from loguru import logger

from api import dependencies
from entities.user import User
from usecases.user.user_usecases import GetProductList, ProductListOperations
from sqlalchemy.exc import IntegrityError
from util.exeptions import UnexpectedDBExeption

router = APIRouter()


@router.post('/product_list')
async def add_product_in_list(tg_id: Annotated[int, Depends(dependencies.user_tg_id)], 
                              product_url: Annotated[str, Body()],
                              usecase: Annotated[ProductListOperations, Depends(dependencies.pl_operations_usecase)]) -> dict[str, str]:
    '''
    Точка для добавления товара в список отслеживания юзера. Если юзера нет в базе - он создается 
    и ему присваивается товар. Если у юзера уже есть этот товар - возвращает ошибку 400
    '''

    try:
        await usecase.execute(tg_id, product_url, add=True)
        logger.success(f'product {product_url} added to {tg_id} product list')
        return {'added': f'{product_url}'}
    
    except IntegrityError:
        logger.error(f'user {tg_id} already have this product')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You have added this product already')
    
    except UnexpectedDBExeption:
        logger.critical(f'unexpected error while adding product {product_url} to {tg_id} product list')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error, plese, try again') 


@router.delete('/product_list')
async def delete_post_in_list(tg_id: Annotated[int, Depends(dependencies.user_tg_id)], 
                              product_url: Annotated[str, Body()],
                              usecase: Annotated[ProductListOperations, Depends(dependencies.pl_operations_usecase)]) -> dict[str, str]:
    '''
    Точка для получения удаления юзера. Проверяет есть ли юзер товар из запроса в базе, если чего то нет - возвращает ошибку 404
    '''
    try:
        await usecase.execute(tg_id, product_url, delete=True)
        logger.success(f'product {product_url} deleted from {tg_id} product list')
        return {'deleted': f'{product_url}'}
    
    except ValueError:
        logger.error(f'user {tg_id} or product {product_url} not found')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User or product not exists')
    

@router.get('/product_list')
async def get_user_products_list(tg_id: Annotated[int, Depends(dependencies.user_tg_id)], 
                                 usecase: Annotated[GetProductList, Depends(dependencies.get_pl_usecase)]) -> User | Exception:
    '''
    Точка для получения списка товаров юзера. Проверяет есть ли юзер в базе, если нет - возвращает ошибку 404
    '''
    try:
        user = await usecase.execute(tg_id)
        logger.success(f'user {tg_id} products list returned')
        return user
    
    except ValueError:
        logger.error(f'user {tg_id} not found')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')


