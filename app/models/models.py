from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from datetime import date


class Author(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[date]

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.first_name!r},"
                f"last_name={self.last_name!r}),")

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
        }


class Book(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id"))
    copies: Mapped[int] = mapped_column(server_default=text('0'))

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}"
                f", title={self.title!r})")

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "author_id": self.author_id,
            "copies": self.copies
        }


class Borrow(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"))
    name: Mapped[str]
    date_of_issue: Mapped[date]
    date_of_return: Mapped[date] = mapped_column(nullable=True)

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}"
                f", date_of_issue={self.date_of_issue!r})")

    def __repr__(self):
        return str(self)
