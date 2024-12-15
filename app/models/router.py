from fastapi import APIRouter, Depends
from app.models.dao import AuthorDAO, BookDAO, BorrowDAO
from app.models.schemas import SAuthor, SBook, SBorrow
from app.models.rb import RBAuthor, RBBook, RBBorrow
from datetime import date

############################
authors_router = APIRouter(prefix="/authors", tags=['Эндпоинты для авторов'])


@authors_router.post('/', summary="Создание автора")
async def add_author(request_body: RBAuthor = Depends()) -> dict:
    check = await AuthorDAO.add(**request_body.to_dict())
    if check:
        return {"message": "Автор создан!", "author": request_body.to_dict()}
    else:
        return {"message": "Ошибка при создании автора!"}


@authors_router.get("/", summary="Получение списка авторов")
async def get_all_authors() -> list[SAuthor]:
    return await AuthorDAO.find_all()


@authors_router.get("/{id}", summary="Получение информации об авторе по id")
async def get_author_by_id(id: int) -> SAuthor | dict:
    rez = await AuthorDAO.find_one_by_id(id)
    if rez is None:
        return {'Message': f'Автор с ID {id} не найден!'}
    return rez


@authors_router.put('/{id}', summary="Обновление информации об авторе")
async def update_author(id: int, request_body: RBAuthor = Depends()) -> dict:
    check = await AuthorDAO.update_by_id(id, **request_body.to_dict())
    if check:
        return {"message": "Информации об авторе обновлена!", "author": request_body.to_dict()}
    else:
        return {"message": "Ошибка при обновлении информации об авторе!"}


@authors_router.delete("/{id}", summary="Удаление автора")
async def delete_author(id: int) -> dict:
    check = await AuthorDAO.delete_by_id(id)
    if check:
        return {"message": f"Автор с ID {id} удален!"}
    else:
        return {"message": "Ошибка при удалении автора!"}

#######################################
books_router = APIRouter(prefix="/books", tags=['Эндпоинты для книг'])


@books_router.post('/', summary="Добавление книги")
async def add_book(request_body: RBBook = Depends()) -> dict:
    book = request_body.to_dict()
    author_id = book["author_id"]
    check = await AuthorDAO.find_one_by_id(author_id)
    if not check:
        return {"message": f"Автор с ID {author_id} не существует!"}
    else:
        check = await BookDAO.add(**book)
        if check:
            return {"message": "Книга добавлена!", "book": book}
        else:
            return {"message": "Ошибка при добавлении книги!"}


@books_router.get("/", summary="Получение списка книг")
async def get_all_books() -> list[SBook]:
    return await BookDAO.find_all()


@books_router.get("/{id}", summary="Получение информации о книге по id")
async def get_book_by_id(id: int) -> SBook | dict:
    rez = await BookDAO.find_one_by_id(id)
    if rez is None:
        return {'Message': f'Книга с ID {id} не найдена!'}
    return rez


@books_router.put('/{id}', summary="Обновление информации о книге")
async def update_book(id: int, request_body: RBBook = Depends()) -> dict:
    book = request_body.to_dict()
    if "author_id" in book:
        author_id = book["author_id"]
        check = await AuthorDAO.find_one_by_id(author_id)
        if not check:
            return {"message": f"Автор с ID {author_id} не существует!"}
    check = await BookDAO.update_by_id(id, **book)
    if check:
        return {"message": "Информации о книге обновлена!", "book": book}
    else:
        return {"message": "Ошибка при обновлении информации о книге!"}


@books_router.delete("/{id}", summary="Удаление книги")
async def delete_book(id: int) -> dict:
    check = await BookDAO.delete_by_id(id)
    if check:
        return {"message": f"Книга с ID {id} удалена!"}
    else:
        return {"message": "Ошибка при удалении книги!"}

#####################################
borrows_router = APIRouter(prefix="/borrows", tags=['Эндпоинты для выдач'])


@borrows_router.post('/', summary="Создание записи о выдаче книги")
async def add_borrow(request_body: RBBorrow = Depends()) -> dict:
    borrow = request_body.to_dict()
    book = await BookDAO.find_one_by_id(borrow["book_id"])
    if not book:
        return {"message": "Книга не существует!"}
    if book.to_dict()["copies"] == 0:
        return {"message": "Книги нет в наличии!"}
    check = await BorrowDAO.add(**borrow)
    if check:
        return {"message": "Записи о выдаче книги создана!", "borrow": borrow}
    else:
        return {"message": "Ошибка при создании записи о выдаче!"}


@borrows_router.get("/", summary="Получение списка всех выдач ")
async def get_all_borrow() -> list[SBorrow]:
    return await BorrowDAO.find_all()


@borrows_router.get("/{id}", summary="Получение информации о выдаче по id")
async def get_borrow_by_id(id: int) -> SBorrow | dict:
    rez = await BorrowDAO.find_one_by_id(id)
    if rez is None:
        return {'Message': f'Выдача с ID {id} не найдена!'}
    return rez


@borrows_router.patch("/{id}/return", summary="Завершение выдачи")
async def update_borrow(id: int, date_of_return: date):
    check = await BorrowDAO.update_by_id(id, **{
        "date_of_return": date_of_return})
    if check:
        return {"message": "Выдача завершена!"}
    else:
        return {"message": "Ошибка при завершении выдачи!"}
