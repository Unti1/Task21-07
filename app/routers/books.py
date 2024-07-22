from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from ..database import get_db
from .. import schemas, models, crud

router = APIRouter()

@router.post("/books/", response_model=schemas.Book)
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_book(db=db, book=book)

@router.get("/books/", response_model=List[schemas.Book])
async def read_books(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    books = await crud.get_books(db, skip=skip, limit=limit)
    return books

@router.get("/books/{book_id}", response_model=schemas.Book)
async def read_book(book_id: int, db: AsyncSession = Depends(get_db)):
    db_book = await crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.put("/books/{book_id}", response_model=schemas.Book)
async def update_book(book_id: int, book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    return await crud.update_book(db=db, book_id=book_id, book=book)

@router.delete("/books/{book_id}", response_model=schemas.Book)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_book(db=db, book_id=book_id)

@router.get("/books/filter/")
async def filter_books(author_id: Optional[int] = None, genre_id: Optional[int] = None, 
                 min_price: Optional[float] = None, max_price: Optional[float] = None, 
                 db: AsyncSession = Depends(get_db)):
    return await crud.filter_books(db, author_id, genre_id, min_price, max_price)