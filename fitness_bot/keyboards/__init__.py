"""
Пакет клавиатур бота.
"""

from .client_kb import get_client_menu
from .trainer_kb import (
    get_trainer_menu,
    get_clients_keyboard,
    get_client_actions_keyboard,
    get_cancel_keyboard,
    get_trainings_list_keyboard,
    get_training_actions_keyboard,
    get_pending_trainings_keyboard,
    get_completion_keyboard
)

__all__ = [
    'get_client_menu',
    'get_trainer_menu',
    'get_clients_keyboard',
    'get_client_actions_keyboard',
    'get_cancel_keyboard',
    'get_trainings_list_keyboard',
    'get_training_actions_keyboard',
    'get_pending_trainings_keyboard',
    'get_completion_keyboard'
]
