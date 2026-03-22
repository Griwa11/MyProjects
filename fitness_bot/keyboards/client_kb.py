"""
Модуль клавиатур для клиентов.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_client_menu() -> ReplyKeyboardMarkup:
    """
    Получить главное меню клиента.

    Returns:
        ReplyKeyboardMarkup: Клавиатура меню клиента
    """
    keyboard = [
        [KeyboardButton(text="📅 Мои тренировки")],
        [KeyboardButton(text="💳 Оплаченные тренировки")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )
