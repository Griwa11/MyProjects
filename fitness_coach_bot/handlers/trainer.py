"""
Модуль обработчиков для тренера.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from config import TRAINER_WELCOME, BOT_USERNAME
from database.models import ClientDB, TrainingDB
from states.client_states import TrainerStates
from keyboards.trainer_kb import (
    get_trainer_menu,
    get_clients_keyboard,
    get_client_actions_keyboard,
    get_cancel_keyboard,
    get_trainings_list_keyboard,
    get_training_actions_keyboard,
    get_pending_trainings_keyboard
)
from keyboards.client_kb import get_client_menu

router = Router()


async def get_pending_count() -> int:
    """
    Получить количество незавершенных тренировок.

    Returns:
        int: Количество тренировок со статусом pending
    """
    pending = await TrainingDB.get_pending_trainings()
    return len(pending)


@router.message(Command("admin"))
async def cmd_admin(message: Message, is_admin: bool, state: FSMContext):
    """
    Команда для входа в панель тренера.

    Args:
        message: Сообщение от пользователя
        is_admin: Флаг прав администратора
        state: Контекст FSM
    """
    if not is_admin:
        await message.answer("❌ У вас нет доступа к этой команде")
        return

    # Очищаем любое активное состояние
    await state.clear()

    # Получаем количество незавершенных
    pending_count = await get_pending_count()

    await message.answer(
        TRAINER_WELCOME,
        reply_markup=get_trainer_menu(pending_count)
    )


@router.message(Command("cancel"))
@router.message(F.text.in_(["❌ Отмена", "Отмена"]))
async def cmd_cancel(message: Message, state: FSMContext, is_admin: bool):
    """
    Отмена текущего действия и возврат в меню.

    Args:
        message: Сообщение от пользователя
        state: Контекст FSM
        is_admin: Флаг прав администратора
    """
    current_state = await state.get_state()

    if current_state is None:
        if is_admin:
            pending_count = await get_pending_count()
            await message.answer(
                "Нечего отменять. Вы в главном меню.",
                reply_markup=get_trainer_menu(pending_count)
            )
        return

    await state.clear()

    if is_admin:
        pending_count = await get_pending_count()
        await message.answer(
            "❌ Действие отменено. Возврат в меню тренера.",
            reply_markup=get_trainer_menu(pending_count)
        )
    else:
        await message.answer("❌ Действие отменено.")


@router.message(F.text == "➕ Добавить клиента")
async def start_add_client(message: Message, state: FSMContext, is_admin: bool):
    """
    Начать процесс добавления нового клиента.
    Отправляет инструкцию, которую тренер может переслать клиенту.

    Args:
        message: Сообщение от тренера
        state: Контекст FSM
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        return

    # Инструкция для клиента (тренер может переслать)
    client_instruction = (
        "📋 <b>Инструкция для регистрации в Fitness Bot</b>\n\n"
        "Чтобы зарегистрироваться, выполните 3 простых шага:\n\n"
        "1️⃣ Кликните на ссылку --> <b>@userinfobot</b>\n"
        "2️⃣ Отправьте боту команду /start\n"
        "3️⃣ Перешлите МНЕ ответное сообщение от @userinfobot\n\n"
        "После этого я добавлю вас в систему ✅"
    )

    await message.answer(
        "📨 <b>Отправьте клиенту эту инструкцию(сообщение ниже⬇️):</b>\n",
        parse_mode="HTML"
    )

    await message.answer(
        client_instruction,
        parse_mode="HTML"
    )

    await message.answer(
        "⏳ Теперь ожидаю от вас пересылку сообщения от @userinfobot с данными клиента.\n\n"
        "Для отмены нажмите кнопку ниже или отправьте /cancel",
        reply_markup=get_cancel_keyboard()
    )

    await state.set_state(TrainerStates.waiting_for_client_id)


@router.message(TrainerStates.waiting_for_client_id)
async def process_client_id(message: Message, state: FSMContext, is_admin: bool):
    """
    Обработка пересланного сообщения от @userinfobot для извлечения ID клиента.

    Args:
        message: Сообщение (пересланное от @userinfobot или текст с ID)
        state: Контекст FSM
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        return

    client_id = None

    # Вариант 1: Пересланное сообщение от userinfobot
    if message.forward_from or message.text:
        text = message.text

        # Ищем строку с Id: или ID: в тексте
        if text:
            lines = text.split('\n')
            for line in lines:
                # Ищем строку содержащую Id:
                if 'Id:' in line or 'ID:' in line or 'id:' in line:
                    # Извлекаем число
                    import re
                    match = re.search(r'\d+', line)
                    if match:
                        client_id = int(match.group())
                        break

    # Вариант 2: Просто число (старый формат для совместимости)
    if not client_id:
        try:
            client_id = int(message.text.strip())
        except ValueError:
            pass

    # Если не нашли ID
    if not client_id:
        await message.answer(
            "❌ Не удалось найти ID клиента!\n\n"
            "Убедитесь что:\n"
            "• Вы пересылаете сообщение от @userinfobot\n"
            "• Или отправляете числовой ID\n\n"
            "Попробуйте еще раз или нажмите Отмена",
            reply_markup=get_cancel_keyboard()
        )
        return

    # Проверяем, не существует ли уже клиент
    if await ClientDB.client_exists(client_id):
        await message.answer(
            f"❌ Клиент с ID {client_id} уже существует в базе!",
            reply_markup=get_cancel_keyboard()
        )
        return

    # Сохраняем ID и запрашиваем имя
    await state.update_data(client_id=client_id)
    await message.answer(
        f"✅ ID клиента получен: <code>{client_id}</code>\n\n"
        "Теперь введите <b>имя и фамилию</b> клиента:\n"
        "Пример: Иван Петров\n\n"
        "Для отмены нажмите кнопку ниже или отправьте /cancel",
        parse_mode="HTML",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(TrainerStates.waiting_for_client_name)


@router.message(TrainerStates.waiting_for_client_name)
async def process_client_name(message: Message, state: FSMContext, is_admin: bool):
    """
    Обработка ввода имени клиента и отправка ссылки на бота.

    Args:
        message: Сообщение с именем
        state: Контекст FSM
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        return

    full_name = message.text.strip()

    if len(full_name) < 2:
        await message.answer(
            "❌ Имя слишком короткое. Попробуйте еще раз:",
            reply_markup=get_cancel_keyboard()
        )
        return

    # Получаем сохраненный ID
    data = await state.get_data()
    client_id = data['client_id']

    # Добавляем клиента в БД
    success = await ClientDB.add_client(client_id, full_name)

    if success:
        pending_count = await get_pending_count()

        await message.answer(
            f"✅ <b>Клиент добавлен в систему!</b>\n\n"
            f"👤 Имя: {full_name}\n"
            f"🆔 ID: <code>{client_id}</code>\n\n"
            f"Теперь клиент может использовать бота.",
            parse_mode="HTML",
            reply_markup=get_trainer_menu(pending_count)
        )

        # Отправляем ссылку на бота для клиента
        bot_link = f"https://t.me/{BOT_USERNAME}"

        await message.answer(
            "📨 <b>Отправьте клиенту эту ссылку:</b>\n\n"
            "Клиент должен открыть бота и нажать START ⬇️",
            parse_mode="HTML"
        )

        await message.answer(
            f"🤖 <b>Ссылка на бота:</b>\n\n"
            f"{bot_link}\n\n"
            f"После того как вы нажмете /start, "
            f"вы сможете пользоваться всеми функциями!",
            parse_mode="HTML"
        )
    else:
        pending_count = await get_pending_count()
        await message.answer(
            "❌ Ошибка при добавлении клиента",
            reply_markup=get_trainer_menu(pending_count)
        )

    await state.clear()


@router.message(F.text == "👥 Клиенты")
async def show_clients_list(message: Message, is_admin: bool):
    """
    Показать список всех клиентов.

    Args:
        message: Сообщение от пользователя
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        return

    clients = await ClientDB.get_all_clients()

    if not clients:
        await message.answer("📭 Клиентов пока нет")
        return

    await message.answer(
        f"👥 Всего клиентов: {len(clients)}\n"
        "Выберите клиента:",
        reply_markup=get_clients_keyboard(clients)
    )


@router.message(F.text == "📅 Показать тренировки")
async def show_all_upcoming_trainings(message: Message, is_admin: bool):
    """
    Показать все предстоящие тренировки всех клиентов.

    Args:
        message: Сообщение от пользователя
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        return

    from datetime import datetime
    import pytz
    from config import TIMEZONE

    # Получаем все будущие тренировки
    all_trainings = await TrainingDB.get_all_upcoming_trainings()

    # Получаем незавершенные
    pending_trainings = await TrainingDB.get_pending_trainings()

    # Получаем текущее время в нужном часовом поясе
    tz = pytz.timezone(TIMEZONE)
    current_time = datetime.now(tz)

    # Фильтруем только будущие тренировки
    upcoming_trainings = []
    for training in all_trainings:
        try:
            # Парсим дату тренировки
            training_dt = datetime.strptime(training['training_datetime'], "%d.%m.%Y %H:%M")
            # Добавляем часовой пояс
            training_dt = tz.localize(training_dt)

            # Если тренировка в будущем - добавляем
            if training_dt > current_time:
                upcoming_trainings.append(training)
        except Exception as e:
            print(f"❌ Ошибка парсинга даты: {e}")
            continue

    # Формируем сообщение
    if not upcoming_trainings and not pending_trainings:
        await message.answer("📅 Нет запланированных и незавершенных тренировок")
        return

    text = ""

    # Блок предстоящих
    if upcoming_trainings:
        text += f"📅 <b>Предстоящие тренировки ({len(upcoming_trainings)}):</b>\n\n"
        for i, training in enumerate(upcoming_trainings, 1):
            username_display = f" (@{training['telegram_username']})" if training.get('telegram_username') else ""
            text += f"{i}. {training['training_datetime']}\n"
            text += f"   👤 {training['client_name']}{username_display}\n\n"

    # Блок незавершенных
    if pending_trainings:
        if text:
            text += "\n" + "="*30 + "\n\n"

        text += f"⚠️ <b>Ожидают завершения ({len(pending_trainings)}):</b>\n\n"

        # Добавляем inline кнопки для быстрого доступа
        await message.answer(text, parse_mode="HTML")

        await message.answer(
            "Выберите тренировку для завершения:",
            reply_markup=get_pending_trainings_keyboard(pending_trainings)
        )
        return

    # Если только предстоящие
    if len(text) > 4000:
        # Разбиваем на несколько сообщений
        messages = []
        current_msg = f"📅 <b>Предстоящие тренировки ({len(upcoming_trainings)}):</b>\n\n"

        for i, training in enumerate(upcoming_trainings, 1):
            username_display = f" (@{training['telegram_username']})" if training.get('telegram_username') else ""
            line = f"{i}. {training['training_datetime']}\n   👤 {training['client_name']}{username_display}\n\n"

            if len(current_msg) + len(line) > 4000:
                messages.append(current_msg)
                current_msg = line
            else:
                current_msg += line

        if current_msg:
            messages.append(current_msg)

        # Отправляем по частям
        for msg in messages:
            await message.answer(msg, parse_mode="HTML")
    else:
        await message.answer(text, parse_mode="HTML")


@router.message(F.text.startswith("⚠️ Незавершенные"))
async def show_pending_trainings(message: Message, is_admin: bool):
    """
    Показать все незавершенные тренировки.

    Args:
        message: Сообщение от пользователя
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        return

    pending_trainings = await TrainingDB.get_pending_trainings()

    if not pending_trainings:
        await message.answer("✅ Нет незавершенных тренировок")
        return

    text = f"⚠️ <b>Незавершенные тренировки ({len(pending_trainings)}):</b>\n\n"
    text += "Выберите тренировку для завершения:"

    await message.answer(text, parse_mode="HTML")
    await message.answer(
        "Нажмите на тренировку:",
        reply_markup=get_pending_trainings_keyboard(pending_trainings)
    )


@router.callback_query(F.data.startswith("client_"))
async def show_client_actions(callback: CallbackQuery, is_admin: bool):
    """
    Показать действия для выбранного клиента.

    Args:
        callback: Callback query
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return

    client_id = int(callback.data.split("_")[1])
    client = await ClientDB.get_client(client_id)

    if not client:
        await callback.answer("❌ Клиент не найден", show_alert=True)
        return

    # Получаем ближайшую тренировку
    nearest = await TrainingDB.get_nearest_training(client_id)
    nearest_text = f"📅 Ближайшая: {nearest['training_datetime']}" if nearest else "📅 Тренировок нет"

    # Проверяем есть ли незавершенные
    pending = await TrainingDB.get_client_pending_trainings(client_id)
    has_pending = len(pending) > 0

    pending_text = f"\n⚠️ Незавершенные: {len(pending)}" if has_pending else ""

    await callback.message.edit_text(
        f"👤 Клиент: {client['full_name']}\n"
        f"🆔 ID: {client['user_id']}\n"
        f"💳 Оплачено тренировок: {client['paid_trainings']}\n"
        f"{nearest_text}{pending_text}\n\n"
        "Выберите действие:",
        reply_markup=get_client_actions_keyboard(client_id, has_pending)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("pending_"))
async def show_client_pending_trainings(callback: CallbackQuery, is_admin: bool):
    """
    Показать незавершенные тренировки клиента.

    Args:
        callback: Callback query
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return

    client_id = int(callback.data.split("_")[1])
    client = await ClientDB.get_client(client_id)
    pending = await TrainingDB.get_client_pending_trainings(client_id)

    if not pending:
        await callback.answer("✅ Нет незавершенных тренировок", show_alert=True)
        return

    text = f"⚠️ <b>Незавершенные тренировки: {client['full_name']}</b>\n\n"

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=get_trainings_list_keyboard(pending, client_id)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("manage_trainings_"))
async def manage_client_trainings(callback: CallbackQuery, is_admin: bool):
    """
    Показать список тренировок клиента для управления.

    Args:
        callback: Callback query
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return

    client_id = int(callback.data.split("_")[2])
    client = await ClientDB.get_client(client_id)
    trainings = await TrainingDB.get_client_trainings(client_id)

    if not trainings:
        await callback.answer("У клиента нет тренировок", show_alert=True)
        return

    text = f"📋 Тренировки: {client['full_name']}\n\n"
    text += "Выберите тренировку для управления:"

    await callback.message.edit_text(
        text,
        reply_markup=get_trainings_list_keyboard(trainings, client_id)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("training_"))
async def show_training_actions(callback: CallbackQuery, is_admin: bool):
    """
    Показать действия для выбранной тренировки.

    Args:
        callback: Callback query
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return

    training_id = int(callback.data.split("_")[1])
    training = await TrainingDB.get_training_by_id(training_id)

    if not training:
        await callback.answer("❌ Тренировка не найдена", show_alert=True)
        return

    client = await ClientDB.get_client(training['client_id'])

    # Статус текстом
    status_map = {
        'scheduled': '📍 Запланирована',
        'pending': '⚠️ Ожидает завершения',
        'completed': '✅ Завершена',
        'cancelled': '❌ Отменена'
    }
    status_text = status_map.get(training['status'], training['status'])

    await callback.message.edit_text(
        f"📅 Тренировка\n\n"
        f"👤 Клиент: {client['full_name']}\n"
        f"📅 Дата: {training['training_datetime']}\n"
        f"Статус: {status_text}\n\n"
        "Выберите действие:",
        reply_markup=get_training_actions_keyboard(training_id, training['client_id'], training['status'])
    )
    await callback.answer()


@router.callback_query(F.data.startswith("confirm_"))
async def confirm_training(callback: CallbackQuery, is_admin: bool):
    """
    Подтвердить завершение тренировки (списать баланс).

    Args:
        callback: Callback query
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return

    training_id = int(callback.data.split("_")[1])
    training = await TrainingDB.get_training_by_id(training_id)

    if not training:
        await callback.answer("❌ Тренировка не найдена", show_alert=True)
        return

    client = await ClientDB.get_client(training['client_id'])

    # Обновляем статус
    await TrainingDB.update_training_status(training_id, 'completed')

    # Списываем баланс
    await ClientDB.decrease_paid_trainings(training['client_id'])

    # Обновляем данные клиента
    client = await ClientDB.get_client(training['client_id'])

    await callback.message.edit_text(
        f"✅ <b>Тренировка подтверждена!</b>\n\n"
        f"👤 Клиент: {client['full_name']}\n"
        f"📅 Дата: {training['training_datetime']}\n"
        f"💳 Баланс списан: -1\n"
        f"💳 Текущий баланс: {client['paid_trainings']}",
        parse_mode="HTML"
    )
    await callback.answer("✅ Тренировка подтверждена, баланс списан")


@router.callback_query(F.data.startswith("decline_"))
async def decline_training(callback: CallbackQuery, is_admin: bool):
    """
    Отменить тренировку (баланс не трогаем).

    Args:
        callback: Callback query
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return

    training_id = int(callback.data.split("_")[1])
    training = await TrainingDB.get_training_by_id(training_id)

    if not training:
        await callback.answer("❌ Тренировка не найдена", show_alert=True)
        return

    client = await ClientDB.get_client(training['client_id'])

    # Обновляем статус
    await TrainingDB.update_training_status(training_id, 'cancelled')

    await callback.message.edit_text(
        f"❌ <b>Тренировка отменена</b>\n\n"
        f"👤 Клиент: {client['full_name']}\n"
        f"📅 Дата: {training['training_datetime']}\n"
        f"💳 Баланс не изменен: {client['paid_trainings']}",
        parse_mode="HTML"
    )
    await callback.answer("❌ Тренировка отменена")


@router.callback_query(F.data.startswith("reschedule_"))
async def start_reschedule_training(callback: CallbackQuery, state: FSMContext, is_admin: bool):
    """
    Начать процесс переноса тренировки.

    Args:
        callback: Callback query
        state: Контекст FSM
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return

    training_id = int(callback.data.split("_")[1])
    training = await TrainingDB.get_training_by_id(training_id)

    if not training:
        await callback.answer("❌ Тренировка не найдена", show_alert=True)
        return

    client = await ClientDB.get_client(training['client_id'])

    # Сохраняем данные в состояние
    await state.update_data(
        training_id=training_id,
        client_id=training['client_id'],
        old_datetime=training['training_datetime']
    )
    await state.set_state(TrainerStates.waiting_for_reschedule_date)

    await callback.message.edit_text(
        f"📅 <b>Перенос тренировки</b>\n\n"
        f"👤 Клиент: {client['full_name']}\n"
        f"📅 Текущая дата: {training['training_datetime']}\n\n"
        f"Введите новую дату и время\n"
        f"Формат: ДД.ММ.ГГГГ ЧЧ:ММ\n"
        f"Пример: 25.12.2024 15:00\n\n"
        f"Для отмены отправьте /cancel",
        parse_mode="HTML"
    )

    await callback.message.answer(
        "Ожидаю новую дату...",
        reply_markup=get_cancel_keyboard()
    )
    await callback.answer()


@router.message(TrainerStates.waiting_for_reschedule_date)
async def process_reschedule_date(message: Message, state: FSMContext, is_admin: bool):
    """
    Обработка ввода новой даты при переносе.

    Args:
        message: Сообщение с новой датой
        state: Контекст FSM
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        return

    from datetime import datetime

    try:
        # Валидация формата даты
        new_datetime = message.text.strip()
        datetime.strptime(new_datetime, "%d.%m.%Y %H:%M")

        # Получаем данные из состояния
        data = await state.get_data()
        training_id = data['training_id']
        client_id = data['client_id']
        old_datetime = data['old_datetime']

        # Отменяем старую тренировку
        await TrainingDB.update_training_status(training_id, 'cancelled')

        # Создаем новую
        await TrainingDB.add_training(client_id, new_datetime)

        client = await ClientDB.get_client(client_id)
        pending_count = await get_pending_count()

        await message.answer(
            f"✅ <b>Тренировка перенесена!</b>\n\n"
            f"👤 Клиент: {client['full_name']}\n"
            f"📅 Было: {old_datetime}\n"
            f"📅 Стало: {new_datetime}\n"
            f"💳 Баланс не изменен: {client['paid_trainings']}",
            parse_mode="HTML",
            reply_markup=get_trainer_menu(pending_count)
        )

        await state.clear()

    except ValueError:
        await message.answer(
            "❌ Неверный формат даты!\n"
            "Используйте формат: ДД.ММ.ГГГГ ЧЧ:ММ\n"
            "Пример: 25.12.2024 15:00\n\n"
            "Для отмены нажмите кнопку ниже или отправьте /cancel",
            reply_markup=get_cancel_keyboard()
        )


@router.callback_query(F.data.startswith("edit_training_"))
async def start_edit_training(callback: CallbackQuery, state: FSMContext, is_admin: bool):
    """
    Начать процесс редактирования тренировки.

    Args:
        callback: Callback query
        state: Контекст FSM
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return

    training_id = int(callback.data.split("_")[2])
    training = await TrainingDB.get_training_by_id(training_id)

    if not training:
        await callback.answer("❌ Тренировка не найдена", show_alert=True)
        return

    # Сохраняем ID тренировки и клиента в состояние
    await state.update_data(training_id=training_id, client_id=training['client_id'])
    await state.set_state(TrainerStates.waiting_for_edit_training_date)

    await callback.message.edit_text(
        f"✏️ Редактирование тренировки\n\n"
        f"Текущая дата: {training['training_datetime']}\n\n"
        f"Введите новую дату и время\n"
        f"Формат: ДД.ММ.ГГГГ ЧЧ:ММ\n"
        f"Пример: 25.12.2024 15:00\n\n"
        f"Для отмены отправьте /cancel"
    )

    # Отправляем новое сообщение с кнопкой отмены
    await callback.message.answer(
        "Ожидаю новую дату тренировки...",
        reply_markup=get_cancel_keyboard()
    )
    await callback.answer()


@router.message(TrainerStates.waiting_for_edit_training_date)
async def process_edit_training_date(message: Message, state: FSMContext, is_admin: bool):
    """
    Обработка ввода новой даты тренировки.

    Args:
        message: Сообщение с датой
        state: Контекст FSM
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        return

    from datetime import datetime

    try:
        # Валидация формата даты
        new_datetime = message.text.strip()
        datetime.strptime(new_datetime, "%d.%m.%Y %H:%M")

        # Получаем ID тренировки из состояния
        data = await state.get_data()
        training_id = data['training_id']
        client_id = data['client_id']

        # Обновляем тренировку
        success = await TrainingDB.update_training_datetime(training_id, new_datetime)

        if success:
            client = await ClientDB.get_client(client_id)
            pending_count = await get_pending_count()

            await message.answer(
                f"✅ Тренировка обновлена!\n"
                f"👤 Клиент: {client['full_name']}\n"
                f"📅 Новая дата: {new_datetime}",
                reply_markup=get_trainer_menu(pending_count)
            )

            # Возвращаемся к карточке клиента
            nearest = await TrainingDB.get_nearest_training(client_id)
            nearest_text = f"📅 Ближайшая: {nearest['training_datetime']}" if nearest else "📅 Тренировок нет"

            pending = await TrainingDB.get_client_pending_trainings(client_id)
            has_pending = len(pending) > 0
            pending_text = f"\n⚠️ Незавершенные: {len(pending)}" if has_pending else ""

            await message.answer(
                f"👤 Клиент: {client['full_name']}\n"
                f"🆔 ID: {client['user_id']}\n"
                f"💳 Оплачено тренировок: {client['paid_trainings']}\n"
                f"{nearest_text}{pending_text}\n\n"
                "Выберите действие:",
                reply_markup=get_client_actions_keyboard(client_id, has_pending)
            )
        else:
            pending_count = await get_pending_count()
            await message.answer(
                "❌ Ошибка при обновлении тренировки",
                reply_markup=get_trainer_menu(pending_count)
            )

        await state.clear()

    except ValueError:
        await message.answer(
            "❌ Неверный формат даты!\n"
            "Используйте формат: ДД.ММ.ГГГГ ЧЧ:ММ\n"
            "Пример: 25.12.2024 15:00\n\n"
            "Для отмены нажмите кнопку ниже или отправьте /cancel",
            reply_markup=get_cancel_keyboard()
        )


@router.callback_query(F.data.startswith("set_training_"))
async def start_set_training(callback: CallbackQuery, state: FSMContext, is_admin: bool):
    """
    Начать процесс назначения тренировки.

    Args:
        callback: Callback query
        state: Контекст FSM
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return

    client_id = int(callback.data.split("_")[2])

    # Сохраняем ID клиента в состояние
    await state.update_data(client_id=client_id)
    await state.set_state(TrainerStates.waiting_for_training_date)

    await callback.message.edit_text(
        "📅 Введите дату и время тренировки\n"
        "Формат: ДД.ММ.ГГГГ ЧЧ:ММ\n"
        "Пример: 25.12.2024 15:00\n\n"
        "Для отмены отправьте /cancel"
    )

    # Отправляем новое сообщение с кнопкой отмены
    await callback.message.answer(
        "Ожидаю дату тренировки...",
        reply_markup=get_cancel_keyboard()
    )
    await callback.answer()


@router.message(TrainerStates.waiting_for_training_date)
async def process_training_date(message: Message, state: FSMContext, is_admin: bool):
    """
    Обработка ввода даты тренировки.

    Args:
        message: Сообщение с датой
        state: Контекст FSM
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        return

    from datetime import datetime

    try:
        # Валидация формата даты
        training_datetime = message.text.strip()
        datetime.strptime(training_datetime, "%d.%m.%Y %H:%M")

        # Получаем ID клиента из состояния
        data = await state.get_data()
        client_id = data['client_id']

        # Добавляем тренировку в БД
        success = await TrainingDB.add_training(client_id, training_datetime)

        if success:
            client = await ClientDB.get_client(client_id)
            pending_count = await get_pending_count()

            await message.answer(
                f"✅ Тренировка назначена!\n"
                f"👤 Клиент: {client['full_name']}\n"
                f"📅 Дата: {training_datetime}",
                reply_markup=get_trainer_menu(pending_count)
            )

            # Возвращаемся к карточке клиента
            nearest = await TrainingDB.get_nearest_training(client_id)
            nearest_text = f"📅 Ближайшая: {nearest['training_datetime']}" if nearest else "📅 Тренировок нет"

            pending = await TrainingDB.get_client_pending_trainings(client_id)
            has_pending = len(pending) > 0
            pending_text = f"\n⚠️ Незавершенные: {len(pending)}" if has_pending else ""

            await message.answer(
                f"👤 Клиент: {client['full_name']}\n"
                f"🆔 ID: {client['user_id']}\n"
                f"💳 Оплачено тренировок: {client['paid_trainings']}\n"
                f"{nearest_text}{pending_text}\n\n"
                "Выберите действие:",
                reply_markup=get_client_actions_keyboard(client_id, has_pending)
            )
        else:
            pending_count = await get_pending_count()
            await message.answer(
                "❌ Ошибка при добавлении тренировки",
                reply_markup=get_trainer_menu(pending_count)
            )

        await state.clear()

    except ValueError:
        await message.answer(
            "❌ Неверный формат даты!\n"
            "Используйте формат: ДД.ММ.ГГГГ ЧЧ:ММ\n"
            "Пример: 25.12.2024 15:00\n\n"
            "Для отмены нажмите кнопку ниже или отправьте /cancel",
            reply_markup=get_cancel_keyboard()
        )


@router.callback_query(F.data.startswith("set_paid_"))
async def start_set_paid(callback: CallbackQuery, state: FSMContext, is_admin: bool):
    """
    Начать процесс установки оплаченных тренировок.

    Args:
        callback: Callback query
        state: Контекст FSM
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return

    client_id = int(callback.data.split("_")[2])

    # Сохраняем ID клиента в состояние
    await state.update_data(client_id=client_id)
    await state.set_state(TrainerStates.waiting_for_paid_count)

    await callback.message.edit_text(
        "💳 Введите количество оплаченных тренировок\n"
        "Пример: 8\n\n"
        "Для отмены отправьте /cancel"
    )

    # Отправляем новое сообщение с кнопкой отмены
    await callback.message.answer(
        "Ожидаю количество тренировок...",
        reply_markup=get_cancel_keyboard()
    )
    await callback.answer()


@router.message(TrainerStates.waiting_for_paid_count)
async def process_paid_count(message: Message, state: FSMContext, is_admin: bool):
    """
    Обработка ввода количества оплаченных тренировок.

    Args:
        message: Сообщение с количеством
        state: Контекст FSM
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        return

    try:
        count = int(message.text.strip())

        if count < 0:
            await message.answer(
                "❌ Количество не может быть отрицательным",
                reply_markup=get_cancel_keyboard()
            )
            return

        # Получаем ID клиента из состояния
        data = await state.get_data()
        client_id = data['client_id']

        # Обновляем в БД
        success = await ClientDB.update_paid_trainings(client_id, count)

        if success:
            client = await ClientDB.get_client(client_id)
            pending_count = await get_pending_count()

            await message.answer(
                f"✅ Обновлено!\n"
                f"👤 Клиент: {client['full_name']}\n"
                f"💳 Оплачено тренировок: {count}",
                reply_markup=get_trainer_menu(pending_count)
            )

            # Возвращаемся к карточке клиента
            nearest = await TrainingDB.get_nearest_training(client_id)
            nearest_text = f"📅 Ближайшая: {nearest['training_datetime']}" if nearest else "📅 Тренировок нет"

            pending = await TrainingDB.get_client_pending_trainings(client_id)
            has_pending = len(pending) > 0
            pending_text = f"\n⚠️ Незавершенные: {len(pending)}" if has_pending else ""

            await message.answer(
                f"👤 Клиент: {client['full_name']}\n"
                f"🆔 ID: {client['user_id']}\n"
                f"💳 Оплачено тренировок: {client['paid_trainings']}\n"
                f"{nearest_text}{pending_text}\n\n"
                "Выберите действие:",
                reply_markup=get_client_actions_keyboard(client_id, has_pending)
            )
        else:
            pending_count = await get_pending_count()
            await message.answer(
                "❌ Ошибка при обновлении",
                reply_markup=get_trainer_menu(pending_count)
            )

        await state.clear()

    except ValueError:
        await message.answer(
            "❌ Введите корректное число\n\n"
            "Для отмены нажмите кнопку ниже или отправьте /cancel",
            reply_markup=get_cancel_keyboard()
        )


@router.callback_query(F.data.startswith("delete_training_"))
async def delete_training(callback: CallbackQuery, is_admin: bool):
    """
    Удалить тренировку.

    Args:
        callback: Callback query
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return

    training_id = int(callback.data.split("_")[2])
    training = await TrainingDB.get_training_by_id(training_id)

    if not training:
        await callback.answer("❌ Тренировка не найдена", show_alert=True)
        return

    client = await ClientDB.get_client(training['client_id'])
    success = await TrainingDB.delete_training(training_id)

    if success:
        await callback.message.edit_text(
            f"✅ Тренировка удалена!\n"
            f"👤 Клиент: {client['full_name']}\n"
            f"📅 Была: {training['training_datetime']}"
        )

        # Показываем карточку клиента
        nearest = await TrainingDB.get_nearest_training(training['client_id'])
        nearest_text = f"📅 Ближайшая: {nearest['training_datetime']}" if nearest else "📅 Тренировок нет"

        pending = await TrainingDB.get_client_pending_trainings(training['client_id'])
        has_pending = len(pending) > 0
        pending_text = f"\n⚠️ Незавершенные: {len(pending)}" if has_pending else ""

        await callback.message.answer(
            f"👤 Клиент: {client['full_name']}\n"
            f"🆔 ID: {client['user_id']}\n"
            f"💳 Оплачено тренировок: {client['paid_trainings']}\n"
            f"{nearest_text}{pending_text}\n\n"
            "Выберите действие:",
            reply_markup=get_client_actions_keyboard(training['client_id'], has_pending)
        )
    else:
        await callback.answer("❌ Ошибка при удалении", show_alert=True)

    await callback.answer()


@router.callback_query(F.data.startswith("delete_client_"))
async def delete_client(callback: CallbackQuery, is_admin: bool):
    """
    Удалить клиента из базы данных.

    Args:
        callback: Callback query
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return

    client_id = int(callback.data.split("_")[2])
    client = await ClientDB.get_client(client_id)

    if not client:
        await callback.answer("❌ Клиент не найден", show_alert=True)
        return

    success = await ClientDB.delete_client(client_id)

    if success:
        await callback.message.edit_text(
            f"✅ Клиент {client['full_name']} удален из базы данных"
        )
    else:
        await callback.answer("❌ Ошибка при удалении", show_alert=True)

    await callback.answer()


@router.callback_query(F.data == "back_to_clients")
async def back_to_clients(callback: CallbackQuery, is_admin: bool):
    """
    Вернуться к списку клиентов.

    Args:
        callback: Callback query
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return

    clients = await ClientDB.get_all_clients()

    await callback.message.edit_text(
        f"👥 Всего клиентов: {len(clients)}\n"
        "Выберите клиента:",
        reply_markup=get_clients_keyboard(clients)
    )
    await callback.answer()


@router.message(F.text == "👤 Режим клиента")
async def switch_to_client_mode(message: Message, is_admin: bool):
    """
    Переключиться в режим клиента (для тестирования).

    Args:
        message: Сообщение от администратора
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        return

    await message.answer(
        "👤 Переключено в режим клиента\n"
        "Для возврата используйте /admin",
        reply_markup=get_client_menu()
    )


@router.message(Command("test_notification"))
async def test_notification(message: Message, is_admin: bool):
    """
    Протестировать систему уведомлений (только для админов).

    Args:
        message: Сообщение от пользователя
        is_admin: Флаг прав администратора
    """
    if not is_admin:
        await message.answer("❌ У вас нет доступа к этой команде")
        return

    from utils.notifications import send_test_notification, check_and_send_notifications, check_and_notify_completed_trainings

    # Отправляем тестовое уведомление
    await send_test_notification(message.bot, message.from_user.id)

    # Также можем запустить проверку уведомлений вручную
    await message.answer(
        "🔍 Запускаю проверку тренировок на завтра...\n"
        "Если есть тренировки, уведомления будут отправлены."
    )

    await check_and_send_notifications(message.bot)

    await message.answer("🔍 Запускаю проверку завершенных тренировок...")
    await check_and_notify_completed_trainings(message.bot)

    await message.answer("✅ Проверка завершена!")
