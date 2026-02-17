import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from infrastructure.db.tables import Base, Product, User

ENGINE = None
async_session = None

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def create_engine(db_data) -> None:
    global ENGINE, async_session
    ENGINE = create_async_engine(db_data, echo=True)

    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Tables created (if they didn't exist)")

    async_session = async_sessionmaker(ENGINE, expire_on_commit=False)
    logger.info('engine create')

async def shut_down_engine() -> None:
    global ENGINE
    if not ENGINE:
        await ENGINE.dispose()
        logger.info('engine shut down')