from app.models.models import Author, Book, Borrow
from app.dao.base import BaseDAO
from app.database import async_session_maker
from sqlalchemy import update, event
from sqlalchemy.exc import SQLAlchemyError


class AuthorDAO(BaseDAO):
    model = Author


class BookDAO(BaseDAO):
    model = Book


class BorrowDAO(BaseDAO):
    model = Borrow

    @event.listens_for(Borrow, 'after_insert')
    def receive_after_insert(mapper, connection, target):
        book_id = target.book_id
        connection.execute(
            update(Book)
            .where(Book.id == book_id)
            .values(copies=Book.copies - 1))

    @classmethod
    async def update_by_id(cls, data_id, **values):
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    update(cls.model)
                    .where(cls.model.id == data_id)
                    .values(**values)
                    .execution_options(synchronize_session="fetch")
                    .returning(cls.model.book_id)
                )
                result = await session.execute(query)
                book_id = result.fetchone()
                query = (
                    update(Book)
                    .where(Book.id == book_id[0])
                    .values(copies=Book.copies + 1)
                )
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount
