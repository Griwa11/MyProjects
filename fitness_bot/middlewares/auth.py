"""
Модуль middleware для проверки прав доступа.
"""

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from config import ADMIN_IDS


class AdminMiddleware(BaseMiddleware):
    """
    Middleware для проверки прав администратора.
    Пропускает только сообщения от пользователей из ADMIN_IDS.
    """

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        """
        Проверка прав доступа перед обработкой события.

        Args:
            handler: Следующий обработчик
            event: Событие (сообщение или callback)
            data: Дополнительные данные

        Returns:
            Any: Результат обработки или None
        """
        user_id = event.from_user.id

        # Добавляем флаг is_admin в данные
        data['is_admin'] = user_id in ADMIN_IDS

        return await handler(event, data)
