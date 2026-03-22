"""
Главный модуль запуска бота.
Точка входа в приложение.
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from config import BOT_TOKEN, TIMEZONE
from database.db import init_db
from handlers import client_router, trainer_router
from middlewares.auth import AdminMiddleware
from utils.notifications import check_and_send_notifications, check_and_notify_completed_trainings


# Глобальная переменная для бота (нужна для планировщика)
bot_instance: Bot = None


async def scheduled_notification_check():
    """
    Обертка для проверки уведомлений (вызывается планировщиком).
    """
    if bot_instance:
        await check_and_send_notifications(bot_instance)


async def scheduled_completion_check():
    """
    Обертка для проверки завершенных тренировок (вызывается планировщиком).
    """
    if bot_instance:
        await check_and_notify_completed_trainings(bot_instance)


async def main():
    """
    Главная функция запуска бота.
    Инициализирует базу данных, настраивает роутеры и запускает polling.
    """
    global bot_instance

    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Инициализация БД
    await init_db()

    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    bot_instance = bot  # Сохраняем для планировщика

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Подключение middleware
    dp.message.middleware(AdminMiddleware())
    dp.callback_query.middleware(AdminMiddleware())

    # Подключение роутеров
    dp.include_router(client_router)
    dp.include_router(trainer_router)

    # Настройка планировщика задач
    scheduler = AsyncIOScheduler(timezone=pytz.timezone(TIMEZONE))

    # Задача 1: Проверка уведомлений о тренировках на завтра (каждый день в 19:00)
    scheduler.add_job(
        scheduled_notification_check,
        trigger=CronTrigger(hour=19, minute=0, timezone=TIMEZONE),
        id='daily_notifications',
        name='Проверка и отправка уведомлений о тренировках на завтра',
        replace_existing=True
    )

    # Задача 2: Проверка завершенных тренировок (каждый час)
    scheduler.add_job(
        scheduled_completion_check,
        trigger=CronTrigger(minute=0, timezone=TIMEZONE),  # Каждый час в :00
        id='hourly_completion_check',
        name='Проверка завершенных тренировок',
        replace_existing=True
    )

    # Запускаем планировщик
    scheduler.start()
    logging.info("⏰ Планировщик уведомлений запущен")
    logging.info("   - Уведомления на завтра: ежедневно в 19:00 МСК")
    logging.info("   - Проверка завершений: каждый час")

    # Запуск бота
    logging.info("🚀 Бот запущен!")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        scheduler.shutdown()
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
