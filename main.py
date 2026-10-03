from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

books = {}
next_id = 1


class Book(BaseModel):
    title: str
    author: str
    price: float


@app.get("/books")
def get_all_books():
    return books


@app.post("/books", status_code=201)
def create_book(book: Book):
    global next_id

    books[next_id] = book.dict()

    next_id += 1

    return books[next_id - 1]