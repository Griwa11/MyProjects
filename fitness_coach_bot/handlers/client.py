"""
Модуль обработчиков для клиентов.
"""

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import WELCOME_MESSAGE
from database.models import ClientDB, TrainingDB
from keyboards.client_kb import get_client_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, is_admin: bool):
    """
    Обработчик команды /start.
    Приветствует пользователя.

    Args:
        message: Сообщение от пользователя
        is_admin: Флаг администратора (из middleware)
    """
    user_id = message.from_user.id

    # Если это админ - показываем специальное приветствие
    if is_admin:
        await message.answer(
            "👨‍💼 Здравствуйте!\n\n"
            "Вы являетесь администратором бота.\n\n"
            "🔧 Для входа в панель тренера используйте команду:\n"
            "/admin\n\n"
            "👤 Также вы можете использовать бота как обычный клиент для тестирования."
        )
        return

    # Проверяем, есть ли клиент в базе
    client = await ClientDB.get_client(user_id)

    if client:
        # Клиент существует
        await message.answer(
            f"👋 Добро пожаловать, {client['full_name']}!\n\n"
            f"💳 Оплачено тренировок: {client['paid_trainings']}\n\n"
            f"Выберите действие из меню:",
            reply_markup=get_client_menu()
        )
    else:
        # Новый пользователь
        await message.answer(
            WELCOME_MESSAGE + "\n\n"
            "⚠️ Вы еще не добавлены в базу клиентов.\n"
            "Обратитесь к тренеру для регистрации."
        )


@router.message(F.text == "📅 Мои тренировки")
async def show_my_trainings(message: Message):
    """
    Показать тренировки клиента.

    Args:
        message: Сообщение от пользователя
    """
    user_id = message.from_user.id

    # Проверяем существование клиента
    client = await ClientDB.get_client(user_id)
    if not client:
        await message.answer("❌ Вы не зарегистрированы. Обратитесь к тренеру.")
        return

    trainings = await TrainingDB.get_client_trainings(user_id)

    if not trainings:
        await message.answer("📅 У вас пока нет запланированных тренировок")
        return

    text = "📅 Ваши тренировки:\n\n"
    for i, training in enumerate(trainings, 1):
        status = "✅ Завершена" if training['is_completed'] else "📍 Запланирована"
        text += f"{i}. {training['training_datetime']} - {status}\n"

    await message.answer(text)


@router.message(F.text == "💳 Оплаченные тренировки")
async def show_paid_trainings(message: Message):
    """
    Показать количество оплаченных тренировок.

    Args:
        message: Сообщение от пользователя
    """
    user_id = message.from_user.id
    client = await ClientDB.get_client(user_id)

    if not client:
        await message.answer("❌ Вы не зарегистрированы. Обратитесь к тренеру.")
        return

    await message.answer(
        f"💳 Оплаченные тренировки\n\n"
        f"У вас осталось: {client['paid_trainings']} тренировок"
    )
