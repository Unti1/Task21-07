from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from .database import Base

book_genre = Table('book_genre', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    pages = Column(Integer)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="books")
    genres = relationship("Genre", secondary=book_genre, back_populates="books")
    bookings = relationship("Booking", back_populates="book")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    avatar = Column(String, nullable=True)

    books = relationship("Book", back_populates="author")
    bookings = relationship("Booking", back_populates="user")

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    books = relationship("Book", secondary=book_genre, back_populates="genres")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    book = relationship("Book", back_populates="bookings")
    user = relationship("User", back_populates="bookings")