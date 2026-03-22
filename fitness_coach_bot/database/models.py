"""
Модуль моделей базы данных.
Содержит все операции с таблицами.
"""

from typing import Optional, List
import aiosqlite
from config import DB_PATH


class ClientDB:
    """Класс для работы с таблицей клиентов."""

    @staticmethod
    async def add_client(user_id: int, full_name: str, telegram_username: str = None) -> bool:
        """
        Добавить нового клиента в базу данных.

        Args:
            user_id: Telegram ID пользователя
            full_name: Полное имя клиента
            telegram_username: Username в Telegram (опционально)

        Returns:
            bool: True если успешно, False при ошибке
        """
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute("""
                    INSERT INTO clients (user_id, full_name, telegram_username)
                    VALUES (?, ?, ?)
                """, (user_id, full_name, telegram_username))
                await db.commit()
                return True
        except Exception as e:
            print(f"❌ Ошибка добавления клиента: {e}")
            return False

    @staticmethod
    async def get_client(user_id: int) -> Optional[dict]:
        """
        Получить информацию о клиенте.

        Args:
            user_id: Telegram ID пользователя

        Returns:
            dict или None: Данные клиента
        """
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM clients WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    @staticmethod
    async def get_all_clients() -> List[dict]:
        """
        Получить список всех клиентов.

        Returns:
            List[dict]: Список всех клиентов
        """
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM clients ORDER BY full_name"
            ) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    @staticmethod
    async def update_paid_trainings(user_id: int, count: int) -> bool:
        """
        Установить количество оплаченных тренировок.

        Args:
            user_id: Telegram ID клиента
            count: Количество оплаченных тренировок

        Returns:
            bool: True если успешно
        """
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute("""
                    UPDATE clients 
                    SET paid_trainings = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                """, (count, user_id))
                await db.commit()
                return True
        except Exception as e:
            print(f"❌ Ошибка обновления тренировок: {e}")
            return False

    @staticmethod
    async def decrease_paid_trainings(user_id: int) -> bool:
        """
        Уменьшить количество оплаченных тренировок на 1.

        Args:
            user_id: Telegram ID клиента

        Returns:
            bool: True если успешно
        """
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute("""
                    UPDATE clients 
                    SET paid_trainings = paid_trainings - 1, 
                        updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                """, (user_id,))
                await db.commit()
                return True
        except Exception as e:
            print(f"❌ Ошибка списания тренировки: {e}")
            return False

    @staticmethod
    async def client_exists(user_id: int) -> bool:
        """
        Проверить существование клиента в базе.

        Args:
            user_id: Telegram ID пользователя

        Returns:
            bool: True если клиент существует
        """
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(
                "SELECT 1 FROM clients WHERE user_id = ?", (user_id,)
            ) as cursor:
                return await cursor.fetchone() is not None

    @staticmethod
    async def delete_client(user_id: int) -> bool:
        """
        Удалить клиента из базы данных.

        Args:
            user_id: Telegram ID клиента

        Returns:
            bool: True если успешно
        """
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                # Удаляем тренировки клиента
                await db.execute("DELETE FROM trainings WHERE client_id = ?", (user_id,))
                # Удаляем клиента
                await db.execute("DELETE FROM clients WHERE user_id = ?", (user_id,))
                await db.commit()
                return True
        except Exception as e:
            print(f"❌ Ошибка удаления клиента: {e}")
            return False


class TrainingDB:
    """Класс для работы с таблицей тренировок."""

    @staticmethod
    async def add_training(client_id: int, training_datetime: str) -> bool:
        """
        Добавить тренировку для клиента.

        Args:
            client_id: Telegram ID клиента
            training_datetime: Дата и время тренировки (формат: "DD.MM.YYYY HH:MM")

        Returns:
            bool: True если успешно
        """
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute("""
                    INSERT INTO trainings (client_id, training_datetime, status)
                    VALUES (?, ?, 'scheduled')
                """, (client_id, training_datetime))
                await db.commit()
                return True
        except Exception as e:
            print(f"❌ Ошибка добавления тренировки: {e}")
            return False

    @staticmethod
    async def get_client_trainings(client_id: int, include_cancelled: bool = False) -> List[dict]:
        """
        Получить все тренировки клиента.

        Args:
            client_id: Telegram ID клиента
            include_cancelled: Включать ли отмененные тренировки

        Returns:
            List[dict]: Список тренировок
        """
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row

            query = """
                SELECT * FROM trainings 
                WHERE client_id = ?
            """

            if not include_cancelled:
                query += " AND status != 'cancelled'"

            query += " ORDER BY training_datetime DESC"

            async with db.execute(query, (client_id,)) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    @staticmethod
    async def get_training_by_id(training_id: int) -> Optional[dict]:
        """
        Получить тренировку по ID.

        Args:
            training_id: ID тренировки

        Returns:
            dict или None: Данные тренировки
        """
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM trainings WHERE id = ?", (training_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    @staticmethod
    async def get_nearest_training(client_id: int) -> Optional[dict]:
        """
        Получить ближайшую БУДУЩУЮ тренировку клиента.

        Args:
            client_id: Telegram ID клиента

        Returns:
            dict или None: Данные ближайшей тренировки
        """
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row

            # Получаем текущее время для сравнения
            from datetime import datetime
            import pytz
            from config import TIMEZONE

            tz = pytz.timezone(TIMEZONE)
            now = datetime.now(tz)
            now_str = now.strftime("%d.%m.%Y %H:%M")

            async with db.execute("""
                SELECT * FROM trainings 
                WHERE client_id = ? 
                  AND status = 'scheduled'
                  AND training_datetime > ?
                ORDER BY training_datetime ASC
                LIMIT 1
            """, (client_id, now_str)) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    @staticmethod
    async def get_all_upcoming_trainings() -> List[dict]:
        """
        Получить все будущие тренировки всех клиентов.

        Returns:
            List[dict]: Список будущих тренировок с информацией о клиентах
        """
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT 
                    t.id,
                    t.training_datetime,
                    t.client_id,
                    t.status,
                    c.full_name as client_name,
                    c.telegram_username
                FROM trainings t
                JOIN clients c ON t.client_id = c.user_id
                WHERE t.status = 'scheduled'
                ORDER BY t.training_datetime ASC
            """) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    @staticmethod
    async def get_pending_trainings() -> List[dict]:
        """
        Получить все тренировки ожидающие завершения.

        Returns:
            List[dict]: Список тренировок со статусом pending
        """
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT 
                    t.id,
                    t.training_datetime,
                    t.client_id,
                    t.status,
                    c.full_name as client_name,
                    c.paid_trainings,
                    c.telegram_username
                FROM trainings t
                JOIN clients c ON t.client_id = c.user_id
                WHERE t.status = 'pending'
                ORDER BY t.training_datetime ASC
            """) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    @staticmethod
    async def get_client_pending_trainings(client_id: int) -> List[dict]:
        """
        Получить незавершенные тренировки конкретного клиента.

        Args:
            client_id: Telegram ID клиента

        Returns:
            List[dict]: Список тренировок со статусом pending
        """
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT * FROM trainings 
                WHERE client_id = ? AND status = 'pending'
                ORDER BY training_datetime DESC
            """, (client_id,)) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    @staticmethod
    async def update_training_datetime(training_id: int, new_datetime: str) -> bool:
        """
        Обновить дату и время тренировки.

        Args:
            training_id: ID тренировки
            new_datetime: Новая дата и время

        Returns:
            bool: True если успешно
        """
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute("""
                    UPDATE trainings 
                    SET training_datetime = ?,
                        status = 'scheduled',
                        notification_sent = 0
                    WHERE id = ?
                """, (new_datetime, training_id))
                await db.commit()
                return True
        except Exception as e:
            print(f"❌ Ошибка обновления тренировки: {e}")
            return False

    @staticmethod
    async def update_training_status(training_id: int, new_status: str) -> bool:
        """
        Обновить статус тренировки.

        Args:
            training_id: ID тренировки
            new_status: Новый статус (scheduled, pending, completed, cancelled)

        Returns:
            bool: True если успешно
        """
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute("""
                    UPDATE trainings 
                    SET status = ?
                    WHERE id = ?
                """, (new_status, training_id))
                await db.commit()
                return True
        except Exception as e:
            print(f"❌ Ошибка обновления статуса: {e}")
            return False

    @staticmethod
    async def mark_notification_sent(training_id: int) -> bool:
        """
        Отметить что уведомление о завершении отправлено.

        Args:
            training_id: ID тренировки

        Returns:
            bool: True если успешно
        """
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute("""
                    UPDATE trainings 
                    SET notification_sent = 1
                    WHERE id = ?
                """, (training_id,))
                await db.commit()
                return True
        except Exception as e:
            print(f"❌ Ошибка обновления notification_sent: {e}")
            return False

    @staticmethod
    async def get_trainings_to_check() -> List[dict]:
        """
        Получить тренировки для проверки (прошедшие час после начала, но еще не pending).

        Returns:
            List[dict]: Список тренировок для проверки
        """
        from datetime import datetime, timedelta
        import pytz
        from config import TIMEZONE

        tz = pytz.timezone(TIMEZONE)
        now = datetime.now(tz)
        one_hour_ago = now - timedelta(hours=1)

        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row

            # Получаем все scheduled тренировки
            async with db.execute("""
                SELECT 
                    t.id,
                    t.training_datetime,
                    t.client_id,
                    t.status,
                    t.notification_sent,
                    c.full_name as client_name,
                    c.paid_trainings
                FROM trainings t
                JOIN clients c ON t.client_id = c.user_id
                WHERE t.status = 'scheduled' AND t.notification_sent = 0
            """) as cursor:
                rows = await cursor.fetchall()

                trainings_to_notify = []
                for row in rows:
                    training = dict(row)
                    try:
                        # Парсим дату тренировки
                        training_dt = datetime.strptime(training['training_datetime'], "%d.%m.%Y %H:%M")
                        training_dt = tz.localize(training_dt)

                        # Если прошло больше часа с начала
                        if training_dt <= one_hour_ago:
                            trainings_to_notify.append(training)
                    except Exception as e:
                        print(f"❌ Ошибка парсинга даты: {e}")
                        continue

                return trainings_to_notify

    @staticmethod
    async def delete_training(training_id: int) -> bool:
        """
        Удалить тренировку.

        Args:
            training_id: ID тренировки

        Returns:
            bool: True если успешно
        """
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute("DELETE FROM trainings WHERE id = ?", (training_id,))
                await db.commit()
                return True
        except Exception as e:
            print(f"❌ Ошибка удаления тренировки: {e}")
            return False
