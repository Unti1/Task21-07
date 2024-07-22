from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, or_
from . import models, schemas
from datetime import datetime

"""
Как варивант можно было создать дирикторию и наделать под каждый из крудов паттерн вроде декоратора
"""


# Book CRUD operations
async def create_book(db: AsyncSession, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump(exclude={'genres'}))
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    
    for genre_id in book.genres:
        genre = await get_genre(db, genre_id)
        if genre:
            db_book.genres.append(genre)
    
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def get_book(db: AsyncSession, book_id: int):
    result = await db.execute(select(models.Book).filter(models.Book.id == book_id))
    return result.scalars().first()

async def get_books(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Book).offset(skip).limit(limit))
    return result.scalars().all()

async def update_book(db: AsyncSession, book_id: int, book: schemas.BookCreate):
    db_book = await get_book(db, book_id)
    if db_book:
        update_data = book.model_dump(exclude={'genres'})
        for key, value in update_data.items():
            setattr(db_book, key, value)
        
        db_book.genres.clear()
        for genre_id in book.genres:
            genre = await get_genre(db, genre_id)
            if genre:
                db_book.genres.append(genre)
        
        await db.commit()
        await db.refresh(db_book)
    return db_book

async def delete_book(db: AsyncSession, book_id: int):
    db_book = await get_book(db, book_id)
    if db_book:
        await db.delete(db_book)
        await db.commit()
    return db_book

async def filter_books(db: AsyncSession, author_id: int = None, genre_id: int = None, 
                       min_price: float = None, max_price: float = None):
    query = select(models.Book)
    conditions = []
    if author_id:
        conditions.append(models.Book.author_id == author_id)
    if genre_id:
        conditions.append(models.Book.genres.any(id=genre_id))
    if min_price is not None:
        conditions.append(models.Book.price >= min_price)
    if max_price is not None:
        conditions.append(models.Book.price <= max_price)
    if conditions:
        query = query.filter(and_(*conditions))
    result = await db.execute(query)
    return result.scalars().all()



# User CRUD operations
async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalars().all()

async def update_user(db: AsyncSession, user_id: int, user: schemas.UserCreate):
    db_user = await get_user(db, user_id)
    if db_user:
        update_data = user.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user(db, user_id)
    if db_user:
        await db.delete(db_user)
        await db.commit()
    return db_user


# Genre CRUD operations
async def create_genre(db: AsyncSession, genre: schemas.GenreCreate):
    db_genre = models.Genre(**genre.model_dump())
    db.add(db_genre)
    await db.commit()
    await db.refresh(db_genre)
    return db_genre

async def get_genre(db: AsyncSession, genre_id: int):
    result = await db.execute(select(models.Genre).filter(models.Genre.id == genre_id))
    return result.scalars().first()

async def get_genres(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Genre).offset(skip).limit(limit))
    return result.scalars().all()

async def update_genre(db: AsyncSession, genre_id: int, genre: schemas.GenreCreate):
    db_genre = await get_genre(db, genre_id)
    if db_genre:
        update_data = genre.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_genre, key, value)
        await db.commit()
        await db.refresh(db_genre)
    return db_genre

async def delete_genre(db: AsyncSession, genre_id: int):
    db_genre = await get_genre(db, genre_id)
    if db_genre:
        await db.delete(db_genre)
        await db.commit()
    return db_genre



# Booking CRUD operations
async def create_booking(db: AsyncSession, booking: schemas.BookingCreate):
    # Check if the book is available for the requested period
    overlapping_bookings = await db.execute(
        select(models.Booking).filter(
            models.Booking.book_id == booking.book_id,
            or_(
                and_(models.Booking.start_date <= booking.start_date, models.Booking.end_date >= booking.start_date),
                and_(models.Booking.start_date <= booking.end_date, models.Booking.end_date >= booking.end_date),
                and_(models.Booking.start_date >= booking.start_date, models.Booking.end_date <= booking.end_date)
            )
        )
    )
    if overlapping_bookings.scalars().first():
        raise ValueError("The book is not available for the requested period")

    db_booking = models.Booking(**booking.model_dump())
    db.add(db_booking)
    await db.commit()
    await db.refresh(db_booking)
    return db_booking

async def get_booking(db: AsyncSession, booking_id: int):
    result = await db.execute(select(models.Booking).filter(models.Booking.id == booking_id))
    return result.scalars().first()

async def get_bookings(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Booking).offset(skip).limit(limit))
    return result.scalars().all()

async def update_booking(db: AsyncSession, booking_id: int, booking: schemas.BookingCreate):
    db_booking = await get_booking(db, booking_id)
    if db_booking:
        update_data = booking.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_booking, key, value)
        await db.commit()
        await db.refresh(db_booking)
    return db_booking

async def delete_booking(db: AsyncSession, booking_id: int):
    db_booking = await get_booking(db, booking_id)
    if db_booking:
        await db.delete(db_booking)
        await db.commit()
    return db_booking

async def remove_expired_bookings(db: AsyncSession):
    current_time = datetime.now()
    expired_bookings = await db.execute(select(models.Booking).filter(models.Booking.end_date < current_time))
    for booking in expired_bookings.scalars().all():
        await db.delete(booking)
    await db.commit()


async def create_book(db: AsyncSession, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def get_books(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Book).offset(skip).limit(limit))
    return result.scalars().all()

async def get_book(db: AsyncSession, book_id: int):
    result = await db.execute(select(models.Book).filter(models.Book.id == book_id))
    return result.scalars().first()

async def update_book(db: AsyncSession, book_id: int, book: schemas.BookCreate):
    db_book = await get_book(db, book_id)
    if db_book:
        for key, value in book.model_dump().items():
            setattr(db_book, key, value)
        await db.commit()
        await db.refresh(db_book)
    return db_book

async def delete_book(db: AsyncSession, book_id: int):
    db_book = await get_book(db, book_id)
    if db_book:
        await db.delete(db_book)
        await db.commit()
    return db_book

async def filter_books(db: AsyncSession, author_id: int = None, genre_id: int = None, 
                       min_price: float = None, max_price: float = None):
    query = select(models.Book)
    conditions = []
    if author_id:
        conditions.append(models.Book.author_id == author_id)
    if genre_id:
        conditions.append(models.Book.genres.any(id=genre_id))
    if min_price is not None:
        conditions.append(models.Book.price >= min_price)
    if max_price is not None:
        conditions.append(models.Book.price <= max_price)
    if conditions:
        query = query.filter(and_(*conditions))
    result = await db.execute(query)
    return result.scalars().all()