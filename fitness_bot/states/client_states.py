"""
Модуль состояний для машины состояний (FSM).
Используется для управления диалогами с пользователями.
"""

from aiogram.fsm.state import State, StatesGroup


class TrainerStates(StatesGroup):
    """Состояния для работы тренера."""

    # Добавление клиента
    waiting_for_client_id = State()
    waiting_for_client_name = State()

    # Назначение тренировки
    waiting_for_training_date = State()

    # Установка оплаченных тренировок
    waiting_for_paid_count = State()

    # Редактирование тренировки
    waiting_for_edit_training_date = State()

    # Перенос тренировки (после подтверждения)
    waiting_for_reschedule_date = State()
