from .base_repository import BaseRepository
from ...data.models.book import Book

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


class BookRepository(BaseRepository[Book]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Book)

    def _apply_filters(self, query, title, author, genre, year, available):
        if title is not None:
            query = query.where(Book.title.ilike(f"%{title}%"))
        if author is not None:
            query = query.where(Book.author.ilike(f"%{author}%"))
        if genre is not None:
            query = query.where(Book.genre.ilike(f"%{genre}%"))
        if year is not None:
            query = query.where(Book.year.ilike(f"%{year}%"))
        if available is not None:
            query = query.where(Book.available.ilike(f"%{available}%"))
        return query

    async def find_by_filters(
            self,
            title: str | None = None,
            author: str | None = None,
            genre: str | None = None,
            year: int | None = None,
            available: bool | None = None,
            limit: int = 20,
            offset: int = 0,
    ) -> list[Book]:
        """Поиск книг с фильтрацией."""
        query = select(Book)
        query = self._apply_filters(query, title, author, genre,year, available)
        query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def find_by_isbn(self, isbn: str) -> Book | None:
        """Найти книгу по ISBN."""
        result = await self.session.execute(
            select(Book).where(Book.isbn == isbn)
        )
        return result.scalar_one_or_none()
        pass

    async def count_by_filters(
            self,
            title: str | None = None,
            author: str | None = None,
            genre: str | None = None,
            year: int | None = None,
            available: bool | None = None,
    ) -> int:
        """Подсчитать количество книг по фильтрам."""
        query = select(func.count()).select_from(Book)
        query = self._apply_filters(query, title, author, genre, year, available)

        result = await self.session.execute(query)
        return result.scalar_one()