from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_db
from .. import schemas, crud

router = APIRouter()

@router.post("/bookings/", response_model=schemas.Booking)
async def create_booking(booking: schemas.BookingCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_booking(db=db, booking=booking)

@router.get("/bookings/", response_model=List[schemas.Booking])
async def read_bookings(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    bookings = await crud.get_bookings(db, skip=skip, limit=limit)
    return bookings

@router.get("/bookings/{booking_id}", response_model=schemas.Booking)
async def read_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    db_booking = await crud.get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

@router.put("/bookings/{booking_id}", response_model=schemas.Booking)
async def update_booking(booking_id: int, booking: schemas.BookingCreate, db: AsyncSession = Depends(get_db)):
    return await crud.update_booking(db=db, booking_id=booking_id, booking=booking)

@router.delete("/bookings/{booking_id}", response_model=schemas.Booking)
async def delete_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_booking(db=db, booking_id=booking_id)