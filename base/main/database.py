from .models import metadata_obj
from .core import async_engine


async def create_tables():
    try:
        async_engine.echo = False
        async with async_engine.begin() as conn:
            await conn.run_sync(metadata_obj.create_all)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        async_engine.echo = False
