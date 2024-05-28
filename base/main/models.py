from sqlalchemy import Table, Column, Integer, String, MetaData, BigInteger

metadata_obj = MetaData()


users_table = Table(
    "users",
    metadata_obj,
    Column("username", String),
    Column("user_id", BigInteger, primary_key=True),
)

videos_table = Table(
    "videos",
    metadata_obj,
    Column("ID", Integer, primary_key=True),
    Column("user_id", BigInteger),
    Column("name", String),
    Column("description", String),
    Column("views", String),
    Column("link", String),
    Column("author", String)
)
