"""
Пакет middleware (промежуточных обработчиков).
"""

from .auth import AdminMiddleware

__all__ = ['AdminMiddleware']
