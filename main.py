from fastapi import FastAPI
from celery import Celery
from app.routers import bookings, books, genres, users
from app.tasks import check_and_remove_expired_bookings
from settings import REDIS_HOST,REDIS_PORT

app = FastAPI()

# Подключаем роутеры
app.include_router(books.router)
app.include_router(users.router)
app.include_router(genres.router)
app.include_router(bookings.router)


# Настройка Celery
celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')

# Конфигурация периодических задач Celery
celery.conf.beat_schedule = {
    'check-expired-bookings': {
        'task': 'site.tasks.check_and_remove_expired_bookings',
        'schedule': 3600.0,  # Запускать каждый час
    },
}

# Регистрация задачи Celery
celery.task(check_and_remove_expired_bookings)