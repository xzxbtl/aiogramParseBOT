import asyncio
import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine
from .config import settings
from .models import users_table

if sys.platform.startswith('win') and os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async_engine = create_async_engine(
    settings.DataBase_URL_psycopg,
    echo=False,
    pool_size=5,
    max_overflow=10,
)


async def get_async_engine_connect():
    async with async_engine.connect() as conn:
        await conn.start(users_table)
    print("Data Base READY FOR WORKING")
