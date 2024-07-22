from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    first_name: str
    last_name: str
    avatar: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class BookBase(BaseModel):
    title: str
    price: float
    pages: int
    author_id: int
    genres: List[int]

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    author: User
    genres: List[Genre]

    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    book_id: int
    user_id: int
    start_date: datetime
    end_date: datetime

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    book: Book
    user: User

    class Config:
        from_attributes = True