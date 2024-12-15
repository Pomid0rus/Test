from datetime import datetime, date
from pydantic import BaseModel, Field, validator
from typing import Optional


class SAuthorAdd(BaseModel):
    first_name: str = Field(..., description="Имя")
    last_name: str = Field(..., description="Фамилия")
    date_of_birth: date = Field(..., description="Дата рождения")

    @validator("date_of_birth")
    def vallidate_date_of_birth(cls, value: date):
        if value and value > datetime.now().date():
            raise ValueError('Некорректная дата')
        return value


class SBookAdd(BaseModel):
    title: str = Field(..., description="Название")
    description: Optional[str] = Field(None, description="Описание")
    author_id: int = Field(..., description="Id автора")
    copies: int = Field(0, description="Количество доступных экземпляров")


class SBorrowAdd(BaseModel):
    book_id: int = Field(..., description="Id книги")
    name: str = Field(..., description="Имя читателя")
    date_of_issue: date = Field(
        datetime.now().date(), description="Дата выдачи")


class SAuthor(BaseModel):
    id: int
    first_name: str = Field(..., description="Имя")
    last_name: str = Field(..., description="Фамилия")
    date_of_birth: date = Field(..., description="Дата рождения")


class SBook(BaseModel):
    id: int
    title: str = Field(..., description="Название")
    description: Optional[str] = Field(None, description="Описание")
    author_id: int = Field(..., description="Id автора")
    copies: int = Field(..., description="Количество доступных экземпляров")


class SBorrow(BaseModel):
    id: int
    book_id: int = Field(..., description="Id книги")
    name: str = Field(..., description="Имя читателя")
    date_of_issue: date = Field(..., description="Дата выдачи")
    date_of_return: Optional[date] = Field(None, description="Дата возврата")

    @validator("date_of_issue")
    def vallidate_date_of_return(cls, value: date):
        if value and value > datetime.now().date():
            raise ValueError('Некорректная дата')
        return value
