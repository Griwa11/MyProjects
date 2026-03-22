"""
Модуль уведомлений о предстоящих тренировках.
Автоматически отправляет уведомления клиентам и тренеру.
"""

import logging
from datetime import datetime, timedelta
import pytz
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List

from config import TIMEZONE, ADMIN_IDS
from database.models import TrainingDB, ClientDB


async def send_client_notification(bot: Bot, client_id: int, training_datetime: str):
    """
    Отправить уведомление клиенту о предстоящей тренировке.

    Args:
        bot: Экземпляр бота
        client_id: Telegram ID клиента
        training_datetime: Дата и время тренировки
    """
    try:
        client = await ClientDB.get_client(client_id)
        if not client:
            return

        message = (
            f"🔔 Напоминание о тренировке!\n\n"
            f"👤 {client['full_name']}\n"
            f"📅 Завтра в {training_datetime.split()[1]}\n"
            f"📍 Дата: {training_datetime}\n\n"
            f"Не забудьте подготовиться к тренировке! 💪"
        )

        await bot.send_message(client_id, message)
        logging.info(f"✅ Уведомление отправлено клиенту {client_id}")

    except Exception as e:
        logging.error(f"❌ Ошибка отправки уведомления клиенту {client_id}: {e}")


async def send_trainer_notification(bot: Bot, trainings: List[dict]):
    """
    Отправить уведомление тренеру о тренировках на завтра.

    Args:
        bot: Экземпляр бота
        trainings: Список тренировок на завтра
    """
    try:
        if not trainings:
            return

        # Формируем сообщение
        message = f"🔔 Расписание на завтра ({len(trainings)} тренировок):\n\n"

        for i, training in enumerate(trainings, 1):
            username_display = f" (@{training['telegram_username']})" if training.get('telegram_username') else ""
            message += (
                f"{i}. {training['training_datetime'].split()[1]} - "
                f"{training['client_name']}{username_display}\n"
            )

        message += "\n💪 Хорошего рабочего дня!"

        # Отправляем всем админам (тренерам)
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(admin_id, message)
                logging.info(f"✅ Уведомление отправлено тренеру {admin_id}")
            except Exception as e:
                logging.error(f"❌ Ошибка отправки тренеру {admin_id}: {e}")

    except Exception as e:
        logging.error(f"❌ Ошибка формирования уведомления для тренера: {e}")


async def check_and_send_notifications(bot: Bot):
    """
    Проверить тренировки на завтра и отправить уведомления.
    Вызывается планировщиком каждый день в 19:00.

    Args:
        bot: Экземпляр бота
    """
    logging.info("🔍 Проверка тренировок на завтра...")

    try:
        # Получаем текущее время
        tz = pytz.timezone(TIMEZONE)
        now = datetime.now(tz)

        # Вычисляем завтрашний день (диапазон 00:00 - 23:59)
        tomorrow_start = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow_end = tomorrow_start.replace(hour=23, minute=59, second=59)

        logging.info(f"📅 Ищем тренировки с {tomorrow_start.strftime('%d.%m.%Y')} по {tomorrow_end.strftime('%d.%m.%Y')}")

        # Получаем все будущие тренировки
        all_trainings = await TrainingDB.get_all_upcoming_trainings()

        # Фильтруем тренировки на завтра
        tomorrow_trainings = []
        client_notifications = {}  # {client_id: training_datetime}

        for training in all_trainings:
            try:
                # Парсим дату тренировки
                training_dt = datetime.strptime(training['training_datetime'], "%d.%m.%Y %H:%M")
                training_dt = tz.localize(training_dt)

                # Проверяем, что тренировка завтра
                if tomorrow_start <= training_dt <= tomorrow_end:
                    tomorrow_trainings.append(training)
                    client_notifications[training['client_id']] = training['training_datetime']

            except Exception as e:
                logging.error(f"❌ Ошибка парсинга даты тренировки: {e}")
                continue

        # Если есть тренировки на завтра
        if tomorrow_trainings:
            logging.info(f"📋 Найдено тренировок на завтра: {len(tomorrow_trainings)}")

            # Отправляем уведомления клиентам
            for client_id, training_datetime in client_notifications.items():
                await send_client_notification(bot, client_id, training_datetime)

            # Отправляем уведомление тренеру
            await send_trainer_notification(bot, tomorrow_trainings)

        else:
            logging.info("📭 Тренировок на завтра нет")

    except Exception as e:
        logging.error(f"❌ Ошибка при проверке уведомлений: {e}")


async def check_and_notify_completed_trainings(bot: Bot):
    """
    Проверить завершенные тренировки и отправить уведомления тренеру.
    Вызывается планировщиком каждый час.

    Args:
        bot: Экземпляр бота
    """
    logging.info("🔍 Проверка завершенных тренировок...")

    try:
        # Получаем тренировки для проверки
        trainings = await TrainingDB.get_trainings_to_check()

        if not trainings:
            logging.info("📭 Нет тренировок требующих подтверждения")
            return

        logging.info(f"📋 Найдено тренировок для подтверждения: {len(trainings)}")

        # Отправляем уведомления тренеру
        for training in trainings:
            await send_completion_request(bot, training)

            # Меняем статус на pending и отмечаем что уведомление отправлено
            await TrainingDB.update_training_status(training['id'], 'pending')
            await TrainingDB.mark_notification_sent(training['id'])

    except Exception as e:
        logging.error(f"❌ Ошибка при проверке завершенных тренировок: {e}")


async def send_completion_request(bot: Bot, training: dict):
    """
    Отправить запрос на подтверждение завершения тренировки.

    Args:
        bot: Экземпляр бота
        training: Данные тренировки
    """
    try:
        # Формируем сообщение
        message = (
            f"🔔 <b>Тренировка завершилась!</b>\n\n"
            f"👤 {training['client_name']}\n"
            f"📅 {training['training_datetime']}\n"
            f"💳 Текущий баланс: {training['paid_trainings']}\n\n"
            f"Подтвердите завершение:"
        )

        # Кнопки
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"confirm_{training['id']}")],
            [InlineKeyboardButton(text="❌ Отменить", callback_data=f"decline_{training['id']}")],
            [InlineKeyboardButton(text="📅 Перенести", callback_data=f"reschedule_{training['id']}")],
        ])

        # Отправляем всем тренерам
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(
                    admin_id,
                    message,
                    parse_mode="HTML",
                    reply_markup=keyboard
                )
                logging.info(f"✅ Запрос на подтверждение отправлен тренеру {admin_id}")
            except Exception as e:
                logging.error(f"❌ Ошибка отправки запроса тренеру {admin_id}: {e}")

    except Exception as e:
        logging.error(f"❌ Ошибка отправки запроса на подтверждение: {e}")


async def send_test_notification(bot: Bot, user_id: int):
    """
    Отправить тестовое уведомление (для проверки работы системы).

    Args:
        bot: Экземпляр бота
        user_id: Telegram ID получателя
    """
    try:
        message = (
            "🔔 Тестовое уведомление\n\n"
            "Система уведомлений работает корректно! ✅\n"
            "Уведомления будут приходить ежедневно в 19:00 по МСК."
        )
        await bot.send_message(user_id, message)
        logging.info(f"✅ Тестовое уведомление отправлено {user_id}")
    except Exception as e:
        logging.error(f"❌ Ошибка отправки тестового уведомления: {e}")
