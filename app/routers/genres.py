from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_db
from .. import schemas, crud

router = APIRouter()

@router.post("/genres/", response_model=schemas.Genre)
async def create_genre(genre: schemas.GenreCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_genre(db=db, genre=genre)

@router.get("/genres/", response_model=List[schemas.Genre])
async def read_genres(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    genres = await crud.get_genres(db, skip=skip, limit=limit)
    return genres

@router.get("/genres/{genre_id}", response_model=schemas.Genre)
async def read_genre(genre_id: int, db: AsyncSession = Depends(get_db)):
    db_genre = await crud.get_genre(db, genre_id=genre_id)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return db_genre

@router.put("/genres/{genre_id}", response_model=schemas.Genre)
async def update_genre(genre_id: int, genre: schemas.GenreCreate, db: AsyncSession = Depends(get_db)):
    return await crud.update_genre(db=db, genre_id=genre_id, genre=genre)

@router.delete("/genres/{genre_id}", response_model=schemas.Genre)
async def delete_genre(genre_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_genre(db=db, genre_id=genre_id)