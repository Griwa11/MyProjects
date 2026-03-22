"""
Пакет обработчиков событий бота.
"""

from .client import router as client_router
from .trainer import router as trainer_router

__all__ = ['client_router', 'trainer_router']
