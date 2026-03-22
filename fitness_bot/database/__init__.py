"""
Пакет для работы с базой данных.
"""

from .db import init_db, get_db
from .models import ClientDB, TrainingDB

__all__ = ['init_db', 'get_db', 'ClientDB', 'TrainingDB']
