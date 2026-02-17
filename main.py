from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.v1 import users_routs, products_routs
from infrastructure.db.engine import create_engine, shut_down_engine
from util.logger import setup_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_engine('postgresql+asyncpg://tracker:1247@localhost/tracker_db')
    yield
    await shut_down_engine()

setup_logger()

app = FastAPI(lifespan=lifespan)

app.include_router(users_routs.router)
app.include_router(products_routs.router)