"""
Модуль клавиатур для тренера.
"""

from typing import List
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)


def get_trainer_menu(pending_count: int = 0) -> ReplyKeyboardMarkup:
    """
    Получить главное меню тренера.

    Args:
        pending_count: Количество незавершенных тренировок

    Returns:
        ReplyKeyboardMarkup: Клавиатура меню тренера
    """
    pending_text = f"⚠️ Незавершенные ({pending_count})" if pending_count > 0 else "⚠️ Незавершенные"

    keyboard = [
        [KeyboardButton(text="👥 Клиенты")],
        [KeyboardButton(text="📅 Показать тренировки")],
        [KeyboardButton(text=pending_text)],
        [KeyboardButton(text="➕ Добавить клиента")],
        [KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="👤 Режим клиента")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Панель тренера..."
    )


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """
    Получить клавиатуру с кнопкой отмены.

    Returns:
        ReplyKeyboardMarkup: Клавиатура с кнопкой отмены
    """
    keyboard = [
        [KeyboardButton(text="❌ Отмена")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Нажмите для отмены..."
    )


def get_clients_keyboard(clients: List[dict]) -> InlineKeyboardMarkup:
    """
    Создать клавиатуру со списком клиентов.

    Args:
        clients: Список клиентов из БД

    Returns:
        InlineKeyboardMarkup: Inline клавиатура со списком
    """
    buttons = []
    for client in clients:
        username_display = f"@{client['telegram_username']}" if client.get('telegram_username') else ""
        buttons.append([
            InlineKeyboardButton(
                text=f"👤 {client['full_name']} {username_display}",
                callback_data=f"client_{client['user_id']}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_client_actions_keyboard(client_id: int, has_pending: bool = False) -> InlineKeyboardMarkup:
    """
    Создать клавиатуру с действиями для выбранного клиента.

    Args:
        client_id: Telegram ID клиента
        has_pending: Есть ли незавершенные тренировки

    Returns:
        InlineKeyboardMarkup: Клавиатура с действиями
    """
    keyboard = [
        [InlineKeyboardButton(text="📅 Назначить тренировку", callback_data=f"set_training_{client_id}")],
        [InlineKeyboardButton(text="💳 Установить оплаченные тренировки", callback_data=f"set_paid_{client_id}")],
        [InlineKeyboardButton(text="📋 Управление тренировками", callback_data=f"manage_trainings_{client_id}")],
    ]

    # Добавляем кнопку незавершенных только если они есть
    if has_pending:
        keyboard.insert(2, [InlineKeyboardButton(
            text="⚠️ Незавершенные тренировки",
            callback_data=f"pending_{client_id}"
        )])

    keyboard.extend([
        [InlineKeyboardButton(text="🗑 Удалить клиента", callback_data=f"delete_client_{client_id}")],
        [InlineKeyboardButton(text="🔙 Назад к списку", callback_data="back_to_clients")],
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_trainings_list_keyboard(trainings: List[dict], client_id: int) -> InlineKeyboardMarkup:
    """
    Создать клавиатуру со списком тренировок клиента.

    Args:
        trainings: Список тренировок
        client_id: Telegram ID клиента

    Returns:
        InlineKeyboardMarkup: Клавиатура со списком тренировок
    """
    buttons = []
    for training in trainings:
        # Иконка в зависимости от статуса
        if training['status'] == 'completed':
            status_icon = "✅"
        elif training['status'] == 'pending':
            status_icon = "⚠️"
        elif training['status'] == 'cancelled':
            status_icon = "❌"
        else:  # scheduled
            status_icon = "📍"

        buttons.append([
            InlineKeyboardButton(
                text=f"{status_icon} {training['training_datetime']}",
                callback_data=f"training_{training['id']}"
            )
        ])

    # Кнопка возврата
    buttons.append([
        InlineKeyboardButton(text="🔙 Назад к клиенту", callback_data=f"client_{client_id}")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_training_actions_keyboard(training_id: int, client_id: int, status: str) -> InlineKeyboardMarkup:
    """
    Создать клавиатуру с действиями для тренировки.

    Args:
        training_id: ID тренировки
        client_id: Telegram ID клиента
        status: Статус тренировки

    Returns:
        InlineKeyboardMarkup: Клавиатура с действиями
    """
    keyboard = []

    # Для scheduled и pending показываем редактирование и удаление
    if status in ['scheduled', 'pending']:
        keyboard.append([InlineKeyboardButton(text="✏️ Изменить дату/время", callback_data=f"edit_training_{training_id}")])
        keyboard.append([InlineKeyboardButton(text="🗑 Удалить тренировку", callback_data=f"delete_training_{training_id}")])

    # Для pending показываем кнопки завершения
    if status == 'pending':
        keyboard.insert(0, [InlineKeyboardButton(text="✅ Подтвердить завершение", callback_data=f"confirm_{training_id}")])
        keyboard.insert(1, [InlineKeyboardButton(text="❌ Отменить тренировку", callback_data=f"decline_{training_id}")])
        keyboard.insert(2, [InlineKeyboardButton(text="📅 Перенести тренировку", callback_data=f"reschedule_{training_id}")])

    # Кнопка назад
    keyboard.append([InlineKeyboardButton(text="🔙 Назад к списку", callback_data=f"manage_trainings_{client_id}")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_pending_trainings_keyboard(trainings: List[dict]) -> InlineKeyboardMarkup:
    """
    Создать клавиатуру со списком незавершенных тренировок.

    Args:
        trainings: Список незавершенных тренировок

    Returns:
        InlineKeyboardMarkup: Клавиатура со списком
    """
    buttons = []
    for training in trainings:
        username_display = f" (@{training['telegram_username']})" if training.get('telegram_username') else ""
        buttons.append([
            InlineKeyboardButton(
                text=f"⚠️ {training['training_datetime']} - {training['client_name']}{username_display}",
                callback_data=f"training_{training['id']}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_completion_keyboard(training_id: int) -> InlineKeyboardMarkup:
    """
    Создать клавиатуру для подтверждения завершения тренировки.

    Args:
        training_id: ID тренировки

    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопками подтверждения
    """
    keyboard = [
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"confirm_{training_id}")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data=f"decline_{training_id}")],
        [InlineKeyboardButton(text="📅 Перенести", callback_data=f"reschedule_{training_id}")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
