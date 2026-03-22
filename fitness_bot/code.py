# ============= ИМПОРТЫ =============
from telebot import TeleBot, types
from telebot.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardRemove)
import config
import database
from datetime import datetime, timedelta
from calendar import monthrange
import re

bot = TeleBot(config.token)

# ============= ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ =============
user_states = {}
calendar_states = {}
selected_clients = {}
temp_questionnaires = {}


# ============= КЛАВИАТУРЫ =============
def main_admin_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("👥 Режим пользователя", "⚙️ Режим админа")
    return markup


def admin_mode_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📋 Список клиентов", "📅 Календарь", "⬅️ Назад")
    return markup


def user_mode_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("👤 Моя анкета", "💪 Оплаченные тренировки", "⏰ Напоминания", "📷 Медиа с тренировок")
    return markup


def client_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        "📝 Показать анкету",
        "💪 Количество тренировок",
        "Напоминания",
        "🔙 Показать список клиентов",
        "🏠 В меню админа"
    )
    return markup


def get_month_keyboard():
    now = datetime.now()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    months = []
    for i in range(-1, 8):
        month_date = now.replace(month=(now.month + i))
        if month_date.month > 12:
            month_date = month_date.replace(year=month_date.year + 1, month=month_date.month - 12)
        elif month_date.month < 1:
            month_date = month_date.replace(year=month_date.year - 1, month=month_date.month + 12)
        months.append((month_date.month, month_date.year))

    unique_months = list(dict.fromkeys(months))
    buttons = [KeyboardButton(datetime(year, month, 1).strftime('%B %Y')) for month, year in unique_months]

    for i in range(0, len(buttons), 3):
        markup.add(*buttons[i:i + 3])
    markup.add(KeyboardButton("🔙 Назад"))
    return markup


def get_day_keyboard(has_events: bool):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("➕ Добавить событие", "➕ Окно тренировки")
    if has_events:
        markup.add("✏️ Редактировать события")
    markup.add("🔙 К выбору дня")
    return markup


# ============= ОСНОВНЫЕ ОБРАБОТЧИКИ =============
@bot.message_handler(commands=['start'])
def start_handler(message: types.Message):
    if message.chat.id in config.admin_id:
        handle_admin_start(message)
    else:
        handle_user_start(message)


# ============= ОБРАБОТЧИКИ АДМИНА =============
def handle_admin_start(message: types.Message):
    bot.send_message(message.chat.id, "⚙️ Меню администратора:", reply_markup=admin_mode_keyboard())


@bot.message_handler(func=lambda m: m.text == "📋 Список клиентов" and m.chat.id in config.admin_id)
def show_clients_list(message: types.Message):
    clients = database.get_all_clients()
    if not clients:
        return bot.send_message(message.chat.id, "❌ Список клиентов пуст")

    markup = InlineKeyboardMarkup()
    for client in clients:
        btn_text = f"{client.first_name} {client.last_name}"
        if client.admin_nickname:
            btn_text += f"\n«{client.admin_nickname}»"
        markup.add(InlineKeyboardButton(btn_text, callback_data=f"client_{client.user_id}"))

    bot.send_message(message.chat.id, "👥 Список клиентов:", reply_markup=markup)


@bot.message_handler(func=lambda m: m.text == "📅 Календарь" and m.chat.id in config.admin_id)
def handle_calendar_start(message: types.Message):
    bot.send_message(message.chat.id, "📅 Выберите месяц:", reply_markup=get_month_keyboard())
    bot.register_next_step_handler(message, process_month_selection)


def process_month_selection(message: types.Message):
    if message.text == "🔙 Назад":
        return handle_admin_start(message)

    try:
        month_name, year = message.text.split()
        month_num = datetime.strptime(month_name, '%B').month
        year = int(year)
        calendar_states[message.chat.id] = {'month': month_num, 'year': year}
        show_day_selection(message, month_num, year)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {str(e)}", reply_markup=get_month_keyboard())


def show_day_selection(message, month, year):
    try:
        busy_days = database.get_busy_days(message.chat.id, year, month)
        _, num_days = monthrange(year, month)
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=7)

        days_buttons = []
        for day in range(1, num_days + 1):
            btn_text = f"🔴 {day}" if day in busy_days else str(day)
            days_buttons.append(KeyboardButton(btn_text))

        for i in range(0, len(days_buttons), 7):
            markup.add(*days_buttons[i:i + 7])
        markup.add(KeyboardButton("🔙 Назад"))

        bot.send_message(
            message.chat.id,
            f"📅 Выберите день в {datetime(year, month, 1).strftime('%B %Y')}:",
            reply_markup=markup
        )
        bot.register_next_step_handler(message, process_day_selection)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {str(e)}", reply_markup=get_month_keyboard())


def process_day_selection(message: types.Message):
    if message.text == "🔙 Назад":
        return handle_calendar_start(message)

    try:
        # Добавляем проверку на наличие текста
        if not message.text:
            raise ValueError("Нет данных для обработки")

        # Исправляем фильтрацию цифр
        day_str = ''.join([c for c in message.text if c.isdigit()])
        if not day_str:
            raise ValueError("Неверный формат дня")

        day = int(day_str)
        state = calendar_states.get(message.chat.id)
        if not state:
            raise ValueError("Сессия устарела")

        _, num_days = monthrange(state['year'], state['month'])
        if not 1 <= day <= num_days:
            raise ValueError("Неверный день")

        calendar_states[message.chat.id]['day'] = day
        selected_date = f"{state['year']}-{state['month']:02d}-{day:02d}"
        events = database.get_events_for_date(message.chat.id, selected_date)

        text = f"📅 {day:02d}.{state['month']:02d}.{state['year']}\n"
        if events:
            events_text = "\n".join([f"⏰ {time}: {desc}" for time, desc in events])
            text += events_text
        else:
            text += "Нет событий"

        bot.send_message(
            message.chat.id,
            text,
            reply_markup=get_day_keyboard(bool(events))
        )
        bot.register_next_step_handler(message, process_day_action)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {str(e)}", reply_markup=get_month_keyboard())


def process_day_action(message: types.Message):
    action_handlers = {
        "🔙 К выбору дня": handle_back_to_days,
        "➕ Добавить событие": handle_add_event,
        "➕ Окно тренировки": show_training_slots_menu,
        "✏️ Редактировать события": handle_edit_events
    }
    handler = action_handlers.get(message.text, handle_unknown_action)
    handler(message)


@bot.message_handler(func=lambda m: m.text == "💪 Количество тренировок" and m.chat.id in config.admin_id)
def handle_trainings_request(message: types.Message):
    client_id = selected_clients.get(message.chat.id)
    if not client_id:
        return bot.send_message(message.chat.id, "❌ Сначала выберите клиента")

    client = database.get_user(client_id)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("✏️ Установить количество", "✅ Тренировка проведена", "🔙 Назад")

    bot.send_message(
        message.chat.id,
        f"Текущее количество тренировок: {client.trainings}",
        reply_markup=markup
    )
    bot.register_next_step_handler(message, process_trainings_action)


def process_trainings_action(message: types.Message):
    if message.text == "🔙 Назад":
        return show_client_menu(message)

    if message.text == "✏️ Установить количество":
        msg = bot.send_message(message.chat.id, "Введите новое количество (0-100):")
        bot.register_next_step_handler(msg, update_trainings_count)
    elif message.text == "✅ Тренировка проведена":
        process_training_completion(message)


def update_trainings_count(message: types.Message):
    try:
        count = int(message.text)
        if not 0 <= count <= 100:
            raise ValueError("Число должно быть от 0 до 100")

        client_id = selected_clients[message.chat.id]
        database.update_trainings(client_id, count)
        bot.send_message(message.chat.id, f"✅ Установлено {count} тренировок", reply_markup=client_menu_keyboard())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {str(e)}")
        bot.register_next_step_handler(message, update_trainings_count)


def handle_add_event(message: types.Message):
    try:
        if not message.text:
            raise ValueError("Пустое сообщение")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            raise ValueError("Нужно указать время и описание")

        time_part, description = parts

        if not re.match(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$', time_part):
            raise ValueError("Неверный формат времени")

        state = calendar_states.get(message.chat.id)
        if not state or 'day' not in state:
            raise ValueError("Дата не выбрана")

        date_str = f"{state['year']}-{state['month']:02d}-{state['day']:02d}"
        database.add_calendar_event(
            admin_id=message.chat.id,
            event_date=date_str,
            event_time=time_part,
            description=description
        )

        bot.send_message(
            message.chat.id,
            f"✅ Событие добавлено: {time_part} - {description}",
            reply_markup=get_day_keyboard(True)
        )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❌ Ошибка: {str(e)}\nПример: 14:30 Стрижка",
            reply_markup=admin_mode_keyboard()
        )


def handle_edit_events(message: types.Message):
    state = calendar_states.get(message.chat.id)
    if not state or 'day' not in state:
        return bot.send_message(message.chat.id, "❌ Дата не выбрана")

    date_str = f"{state['year']}-{state['month']:02d}-{state['day']:02d}"
    events = database.get_events_for_date(message.chat.id, date_str)

    if not events:
        return bot.send_message(message.chat.id, "Нет событий для редактирования")

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for time, desc in events:
        markup.add(f"✏️ {time} - {desc[:15]}...")
    markup.add("🔙 Назад")

    bot.send_message(message.chat.id, "Выберите событие:", reply_markup=markup)
    bot.register_next_step_handler(message, process_event_selection)


def show_client_menu(message: types.Message):
    client_id = selected_clients.get(message.chat.id)
    if client_id:
        bot.send_message(
            message.chat.id,
            "👤 Меню клиента:",
            reply_markup=client_menu_keyboard()
        )


def process_training_completion(message: types.Message):
    client_id = selected_clients.get(message.chat.id)
    if not client_id:
        return

    conn = database.create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET trainings = trainings - 1 WHERE user_id = ?', (client_id,))
        conn.commit()
        bot.send_message(
            message.chat.id,
            "✅ Тренировка отмечена как проведенная",
            reply_markup=client_menu_keyboard()
        )
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {str(e)}")
    finally:
        conn.close()


# ============= ОБРАБОТЧИКИ ПОЛЬЗОВАТЕЛЕЙ =============
def handle_user_start(message: types.Message):
    user = database.get_user(message.chat.id)
    if user:
        bot.send_message(message.chat.id, "🏋️ Добро пожаловать!", reply_markup=user_mode_keyboard())
    else:
        start_questionnaire(message)


@bot.message_handler(func=lambda m: m.text == "👤 Моя анкета")
def show_my_questionnaire(message: types.Message):
    user = database.get_user(message.chat.id)
    if user:
        text = f"📄 Анкета:\n\n👤 {user.first_name} {user.last_name}\n🎂 Возраст: {user.age}\n⚖️ Вес: {user.weight}\n📏 Рост: {user.height}\n🏥 Противопоказания: {user.medical_conditions}\n🎯 Цель: {user.training_goal}\n🏅 Опыт: {user.sport_history}\n📅 Тренировки: {user.training_frequency}/неделю"
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, "❌ Анкета не найдена")


# ============= РАБОТА С АНКЕТОЙ =============
def start_questionnaire(message):
    user_id = message.chat.id
    user_states[user_id] = {'step': 0, 'data': {}}
    ask_question(user_id)


def ask_question(user_id):
    state = user_states[user_id]
    question = [
        "👋 Привет! Давайте заполним анкету!\n1. Введите имя и фамилию через пробел:",
        "2. Введите возраст, вес и рост (через пробел, пример: 25 70 180):",
        "3. Есть ли у вас медицинские противопоказания?",
        "4. Какая у вас цель тренировок?",
        "5. Как давно занимались спортом?",
        "6. Сколько раз в неделю готовы тренироваться?"
    ][state['step']]

    bot.send_message(user_id, question)
    bot.register_next_step_handler_by_chat_id(user_id, handle_questionnaire_answer)


def handle_questionnaire_answer(message: types.Message):
    user_id = message.chat.id
    state = user_states.get(user_id)
    if not state:
        return bot.send_message(user_id, "❌ Сессия устарела, начните заново /start")

    try:
        step = state['step']
        if step == 0:
            fname, lname = message.text.split(maxsplit=1)
            state['data'] = {'first_name': fname, 'last_name': lname}
        elif step == 1:
            age, weight, height = map(float, message.text.split())
            state['data'].update({'age': age, 'weight': weight, 'height': height})
        else:
            state['data'][
                ['medical_conditions', 'training_goal', 'sport_history', 'training_frequency'][step - 2]] = message.text

        state['step'] += 1
        if state['step'] < 6:
            ask_question(user_id)
        else:
            database.create_user(database.User(user_id=user_id, **state['data']))
            del user_states[user_id]
            bot.send_message(user_id, "✅ Анкета заполнена!", reply_markup=user_mode_keyboard())
    except Exception as e:
        bot.send_message(user_id, f"❌ Ошибка: {str(e)}\nПопробуйте еще раз")
        ask_question(user_id)


# ============= ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =============
def show_training_slots_menu(message: types.Message):
    state = calendar_states.get(message.chat.id)
    if not state or 'day' not in state:
        return bot.send_message(message.chat.id, "❌ Дата не выбрана")

    selected_date = f"{state['year']}-{state['month']:02d}-{state['day']:02d}"
    busy_slots = database.get_busy_slots(message.chat.id, selected_date)

    markup = InlineKeyboardMarkup(row_width=3)
    buttons = []
    for hour in range(7, 23):
        time_slot = f"{hour:02d}:00-{(hour + 1):02d}:00"
        if time_slot.split('-')[0] not in busy_slots:
            buttons.append(InlineKeyboardButton(time_slot, callback_data=f"slot_{time_slot}"))

    for i in range(0, len(buttons), 3):
        markup.add(*buttons[i:i + 3])
    markup.add(InlineKeyboardButton("❌ Отмена", callback_data="cancel_slots"))

    bot.send_message(message.chat.id, "🕒 Выберите время:", reply_markup=markup)


def handle_back_to_days(message: types.Message):
    state = calendar_states.get(message.chat.id)
    if state:
        show_day_selection(message, state['month'], state['year'])
    else:
        handle_calendar_start(message)


def handle_unknown_action(message: types.Message):
    bot.send_message(message.chat.id, "⚠️ Неизвестная команда", reply_markup=admin_mode_keyboard())


# ============= ЗАПУСК БОТА =============
if __name__ == '__main__':
    print("🤖 Бот запущен!")
    bot.infinity_polling()