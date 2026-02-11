from fastapi import FastAPI

from api.v1 import users_routs, products_routs

app = FastAPI()

app.include_router(users_routs.router)
app.include_router(products_routs.router)