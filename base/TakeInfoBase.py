from aiogrambot.base.main.core import async_engine
from aiogrambot.base.main.models import videos_table


class TakeInfo:

    @staticmethod
    async def insert_video_parse_info(user_id, titles, views, links, desk, authors):
        async with async_engine.begin() as conn:
            stmt_check = videos_table.select().where(
                videos_table.c.link == links,
                videos_table.c.user_id == user_id
            )
            result = await conn.execute(stmt_check)
            if not result.fetchone():
                stmt_update = videos_table.insert().values(user_id=user_id,
                                                           name=titles, views=views,
                                                           link=links, description=desk, author=authors)
                await conn.execute(stmt_update)

    @staticmethod
    async def get_buttons_with_last_authors(user_id):
        async with async_engine.begin() as conn:
            query = videos_table.select().where(videos_table.c.user_id == user_id).with_only_columns(
                videos_table.c.author,
            ).distinct()
            result = await conn.execute(query)
            row = result.fetchall()

            return row

    @staticmethod
    async def clean_parses_info(user_id):
        async with async_engine.begin() as conn:
            await conn.execute(videos_table.delete().where(videos_table.c.user_id == user_id))

    @staticmethod
    async def select_video_parse_titles(user_id, author):
        async with async_engine.begin() as conn:
            query = videos_table.select().where(
                (videos_table.c.user_id == user_id) & (videos_table.c.author == author)).with_only_columns(
                videos_table.c.name,
            )
            result = await conn.execute(query)
            row = result.fetchall()
            return row

    @staticmethod
    async def select_last_video_parse_titles_by_last_author(user_id):
        async with async_engine.begin() as conn:
            subquery = videos_table.select().where(videos_table.c.user_id == user_id).order_by(
                videos_table.c.ID.desc()
            ).limit(1).with_only_columns(videos_table.c.author)
            query = videos_table.select().where(
                videos_table.c.author.in_(subquery) & (videos_table.c.user_id == user_id)
            ).with_only_columns(videos_table.c.name)
            result = await conn.execute(query)
            row = result.fetchall()
            return row

    @staticmethod
    async def select_last_video_parse_views_by_last_author(user_id):
        async with async_engine.begin() as conn:
            subquery = videos_table.select().where(videos_table.c.user_id == user_id).order_by(
                videos_table.c.ID.desc()
            ).limit(1).with_only_columns(videos_table.c.author)
            query = videos_table.select().where(
                videos_table.c.author.in_(subquery) & (videos_table.c.user_id == user_id)
            ).with_only_columns(videos_table.c.views)
            result = await conn.execute(query)
            row = result.fetchall()
            return row

    @staticmethod
    async def select_last_video_parse_link_by_last_author(user_id):
        async with async_engine.begin() as conn:
            subquery = videos_table.select().where(videos_table.c.user_id == user_id).order_by(
                videos_table.c.ID.desc()
            ).limit(1).with_only_columns(videos_table.c.author)
            query = videos_table.select().where(
                videos_table.c.author.in_(subquery) & (videos_table.c.user_id == user_id)
            ).with_only_columns(videos_table.c.link)
            result = await conn.execute(query)
            row = result.fetchall()
            return row

    @staticmethod
    async def select_last_video_parse_description_by_last_author(user_id):
        async with async_engine.begin() as conn:
            subquery = videos_table.select().where(videos_table.c.user_id == user_id).order_by(
                videos_table.c.ID.desc()
            ).limit(1).with_only_columns(videos_table.c.author)
            query = videos_table.select().where(
                videos_table.c.author.in_(subquery) & (videos_table.c.user_id == user_id)
            ).with_only_columns(videos_table.c.description)
            result = await conn.execute(query)
            row = result.fetchall()
            return row

    @staticmethod
    async def select_video_parse_views(user_id, author):
        async with async_engine.begin() as conn:
            query = videos_table.select().where(
                (videos_table.c.user_id == user_id) & (videos_table.c.author == author)).with_only_columns(
                videos_table.c.views,
            )
            result = await conn.execute(query)
            row = result.fetchall()
            return row

    @staticmethod
    async def select_video_parse_links(user_id, author):
        async with async_engine.begin() as conn:
            query = videos_table.select().where(
                (videos_table.c.user_id == user_id) & (videos_table.c.author == author)).with_only_columns(
                videos_table.c.link,
            )
            result = await conn.execute(query)
            row = result.fetchall()
            return row

    @staticmethod
    async def select_video_parse_description(user_id, author):
        async with async_engine.begin() as conn:
            query = videos_table.select().where(
                (videos_table.c.user_id == user_id) & (videos_table.c.author == author)).with_only_columns(
                videos_table.c.description,
            )
            result = await conn.execute(query)
            row = result.fetchall()
            return row
