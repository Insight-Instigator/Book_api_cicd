from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData

metadata = MetaData()

books = Table(
    "books",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("title", String, nullable=False),
    Column("author", String, nullable=False),
    Column("published_year", Integer, nullable=False),
    Column("genre", String, nullable=True),
    Column("available", Boolean, default=True)
)
