import mysql.connector
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# Данные для подключения к MySQL
db_config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'tech_support',
}

# Инициализация базы данных
def init_db():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE()")
    db = cursor.fetchone()
    print(f"Connected to database: {db}")
    cursor.close()
    conn.close()

# Состояния для обработки сообщений
GREETING, NAME, BUILDING, ROOM, COMMENT = range(5)

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Здравствуйте! Как я могу помочь? Выберите:\n"
        "1. Подать заявку\n"
        "2. Проверить статус заявки\n"
        "3. Позвать техника"
    )
    return GREETING

def greeting(update: Update, context: CallbackContext) -> int:
    choice = update.message.text
    if choice == '1':
        update.message.reply_text('Пожалуйста, введите ваше ФИО:')
        return NAME
    elif choice == '2':
        update.message.reply_text('Эта функция еще не реализована.')
        return ConversationHandler.END
    elif choice == '3':
        update.message.reply_text('Позвать техника еще не реализовано.')
        return ConversationHandler.END
    else:
        update.message.reply_text('Неверный выбор. Попробуйте еще раз.')
        return GREETING

def request_name(update: Update, context: CallbackContext) -> int:
    context.user_data['name'] = update.message.text
    update.message.reply_text('Выберите корпус (старший или младший):')
    return BUILDING

def request_building(update: Update, context: CallbackContext) -> int:
    context.user_data['building'] = update.message.text
    update.message.reply_text('Введите номер кабинета:')
    return ROOM

def request_room(update: Update, context: CallbackContext) -> int:
    context.user_data['room'] = update.message.text
    update.message.reply_text('Хотите добавить комментарий? (да/нет):')
    return COMMENT

def request_comment(update: Update, context: CallbackContext) -> int:
    comment_choice = update.message.text.lower()
    if comment_choice == 'да':
        update.message.reply_text('Введите ваш комментарий:')
        return COMMENT
    else:
        context.user_data['comment'] = ''
        save_request_to_db(context.user_data)
        update.message.reply_text('Ваша заявка принята.')
        return ConversationHandler.END

def get_comment(update: Update, context: CallbackContext) -> int:
    context.user_data['comment'] = update.message.text
    save_request_to_db(context.user_data)
    update.message.reply_text('Ваша заявка принята.')
    return ConversationHandler.END

def save_request_to_db(data):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO requests (full_name, building, room, comment) VALUES (%s, %s, %s, %s)",
        (data['name'], data['building'], data['room'], data['comment'])
    )
    conn.commit()
    cursor.close()
    conn.close()

def main():
    # Инициализация бота
    updater = Updater("YOUR TELEGRAM BOT TOKEN")
    dispatcher = updater.dispatch