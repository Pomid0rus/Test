from fastapi import FastAPI
from app.models.router import authors_router, books_router, borrows_router


app = FastAPI()
app.include_router(authors_router)
app.include_router(books_router)
app.include_router(borrows_router)
