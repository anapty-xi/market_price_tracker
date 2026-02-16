from fastapi import APIRouter, HTTPException, status, Depends, Body
from typing import Annotated

from api import dependencies
from entities.user import User
from usecases.user.user_usecases import GetProductList, ProductListOperations
from sqlalchemy.exc import IntegrityError
from util.exeptions import UnexpectedDBExeption

router = APIRouter()


@router.post('/products')
async def add_product_in_list(tg_id: Annotated[int, Depends(dependencies.user_tg_id)], 
                              product_url: Annotated[str, Body()],
                              usecase: Annotated[ProductListOperations, Depends(dependencies.pl_operations_usecase)]) -> dict[str, str]:
    try:
        await usecase.execute(tg_id, product_url, add=True)
        return {'added': f'{product_url}'}
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You have added this product already')
    except UnexpectedDBExeption:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error, plese, try again') 

@router.get('/products')
async def get_user_products_list(tg_id: Annotated[int, Depends(dependencies.user_tg_id)], 
                                 usecase: Annotated[GetProductList, Depends(dependencies.get_pl_usecase)]) -> User:
    try:
        user = await usecase.execute(tg_id)
        return user
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

@router.delete('/products')
async def delete_post_in_list(tg_id: Annotated[int, Depends(dependencies.user_tg_id)], 
                              product_url: Annotated[str, Body()],
                              usecase: Annotated[ProductListOperations, Depends(dependencies.pl_operations_usecase)]) -> dict[str, str]:
    try:
        await usecase.execute(tg_id, product_url, delete=True)
        return {'deleted': f'{product_url}'}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User or product not exists')