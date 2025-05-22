from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import books
from typing import List, Dict, Optional

class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_books(self) -> List[Dict]:
        result = await self.session.execute(select(books))
        return [dict(row._mapping) for row in result.fetchall()]

    async def get_book_by_id(self, book_id: int) -> Optional[Dict]:
        result = await self.session.execute(select(books).where(books.c.id == book_id))
        book = result.first()
        return dict(book._mapping) if book else None

    async def create_book(self, book_data: Dict) -> Dict:
        query = books.insert().values(**book_data)
        result = await self.session.execute(query)
        await self.session.commit()
        return {**book_data, "id": result.inserted_primary_key[0]}

    async def update_book(self, book_id: int, book_data: Dict) -> Optional[Dict]:
        query = books.update().where(books.c.id == book_id).values(**book_data)
        result = await self.session.execute(query)
        await self.session.commit()
        return {**book_data, "id": book_id} if result.rowcount > 0 else None

    async def delete_book(self, book_id: int) -> bool:
        query = books.delete().where(books.c.id == book_id)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0 