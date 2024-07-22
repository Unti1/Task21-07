from celery import Celery
from datetime import datetime

from settings import REDIS_HOST, REDIS_PORT
from .database import AsyncSessionLocal
from .models import Booking
from sqlalchemy.future import select
import asyncio

celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')

@celery.task
def check_and_remove_expired_bookings():
    asyncio.run(_check_and_remove_expired_bookings())

async def _check_and_remove_expired_bookings():
    async with AsyncSessionLocal() as db:
        current_time = datetime.now()
        query = select(Booking).filter(Booking.end_date < current_time)
        result = await db.execute(query)
        expired_bookings = result.scalars().all()
        for booking in expired_bookings:
            await db.delete(booking)
        await db.commit()