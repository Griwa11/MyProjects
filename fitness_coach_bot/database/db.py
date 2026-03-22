"""
Модуль инициализации и управления подключением к базе данных.
"""

import aiosqlite
from config import DB_PATH


async def init_db():
    """
    Инициализация базы данных.
    Создает необходимые таблицы, если их нет.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        # Таблица клиентов (упрощенная)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT NOT NULL,
                telegram_username TEXT,
                paid_trainings INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Таблица тренировок
        await db.execute("""
            CREATE TABLE IF NOT EXISTS trainings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                training_datetime TEXT NOT NULL,
                status TEXT DEFAULT 'scheduled',
                notification_sent INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients (user_id)
            )
        """)

        # Проверяем существует ли колонка status (для миграции старых БД)
        async with db.execute("PRAGMA table_info(trainings)") as cursor:
            columns = await cursor.fetchall()
            column_names = [col[1] for col in columns]

            # Если нет колонки status - добавляем
            if 'status' not in column_names:
                await db.execute("ALTER TABLE trainings ADD COLUMN status TEXT DEFAULT 'scheduled'")
                print("✅ Добавлено поле status в таблицу trainings")

            # Если нет колонки notification_sent - добавляем
            if 'notification_sent' not in column_names:
                await db.execute("ALTER TABLE trainings ADD COLUMN notification_sent INTEGER DEFAULT 0")
                print("✅ Добавлено поле notification_sent в таблицу trainings")

            # Если есть старое поле is_completed - мигрируем данные
            if 'is_completed' in column_names:
                # Переносим данные: is_completed=1 -> status='completed', is_completed=0 -> status='scheduled'
                await db.execute("""
                    UPDATE trainings 
                    SET status = CASE 
                        WHEN is_completed = 1 THEN 'completed'
                        ELSE 'scheduled'
                    END
                    WHERE status IS NULL OR status = ''
                """)
                print("✅ Мигрированы данные из is_completed в status")

        await db.commit()
        print("✅ База данных инициализирована")


async def get_db():
    """
    Получить подключение к базе данных.

    Returns:
        aiosqlite.Connection: Подключение к БД
    """
    return await aiosqlite.connect(DB_PATH)
