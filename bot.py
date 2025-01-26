import telebot
import mysql.connector
# Подключение к базе данных MySQL
db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="password",
    database="support_bot_db"
)

cursor = db.cursor()

# Создание бота
bot = telebot.TeleBot('Вставь свой токен')

user_data = {}
def save_request(user_id):
    cursor.execute("INSERT INTO requests (full_name, building, room, comment) VALUES (%s, %s, %s, %s)",
                   (user_data[user_id]['full_name'], user_data[user_id]['building'], user_data[user_id]['room'],
                    user_data[user_id]['comment']))
    db.commit()

def clear_user_data(user_id):
    user_data[user_id] = {'stage': 'greet'}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    clear_user_data(user_id)
    bot.reply_to(message,
                 "Привет. Что вы хотите сделать?\n1. Подать заявку\n2. Провести статус заявки\n3. Позвать техника")

@bot.message_handler(func=lambda message: user_data[message.chat.id]['stage'] == 'greet')
def handle_greet(message):
    user_id = message.chat.id
    if message.text == '1':
        user_data[user_id]['stage'] = 'full_name'
        bot.reply_to(message, "Пожалуйста, введите ваше ФИО.")
    elif message.text == '2':
        bot.reply_to(message, "Проверка статуса: введите ID заявки.")
        user_data[user_id]['stage'] = 'check_status'
    elif message.text == '3':
        bot.reply_to(message, "Техник вызван. Пожалуйста, общайтесь через бота.")

@bot.message_handler(func=lambda message: user_data[message.chat.id]['stage'] == 'full_name')
def handle_full_name(message):
    user_id = message.chat.id
    user_data[user_id]['full_name'] = message.text
    user_data[user_id]['stage'] = 'building'
    bot.reply_to(message, "Выберите корпус (старший или младший).")

@bot.message_handler(func=lambda message: user_data[message.chat.id]['stage'] == 'building')
def handle_building(message):
    user_id = message.chat.id
    user_data[user_id]['building'] = message.text
    user_data[user_id]['stage'] = 'room'
    bot.reply_to(message, "Пожалуйста, введите номер кабинета.")

@bot.message_handler(func=lambda message: user_data[message.chat.id]['stage'] == 'room')
def handle_room(message):
    user_id = message.chat.id
    user_data[user_id]['room'] = message.text
    user_data[user_id]['stage'] = 'comment_choice'
    bot.reply_to(message, "Хотите добавить комментарий? (да/нет)")

@bot.message_handler(func=lambda message: user_data[message.chat.id]['stage'] == 'comment_choice')
def handle_comment_choice(message):
    user_id = message.chat.id
    if message.text.lower() == 'да':
        user_data[user_id]['stage'] = 'comment'
        bot.reply_to(message, "Пожалуйста, введите ваш комментарий.")
    else:
        user_data[user_id]['comment'] = ''
        save_request(user_id)
        bot.reply_to(message, "Ваша заявка принята.")
        cursor.execute("SELECT id FROM requests")
        result = cursor.fetchall()
        ids = [row[0] for row in result]
        message = ids[-1]
        bot.send_message(user_id, "Номер вашей заявки: "+str(message))
        clear_user_data(user_id)

@bot.message_handler(func=lambda message: user_data[message.chat.id]['stage'] == 'comment')
def handle_comment(message):
    user_id = message.chat.id
    user_data[user_id]['comment'] = message.text
    save_request(user_id)
    bot.reply_to(message, "Ваша заявка принята.")
    cursor.execute("SELECT id FROM requests")
    result = cursor.fetchall()
    ids = [row[0] for row in result]
    message = ids[-1]
    bot.send_message(user_id, "Номер вашей заявки: "+str(message))
    clear_user_data(user_id)

@bot.message_handler(func=lambda message: user_data[message.chat.id]['stage'] == 'check_status')
def handle_room(message):
    user_id = message.chat.id
    a = message.text
    query = "SELECT status FROM requests WHERE id = %s" % a
    cursor.execute(query)
    result = cursor.fetchall()
    bot.send_message(user_id,"Статус вашей заявки: "+ str(result))

bot.polling()
cursor.execute("SELECT * FROM requests")

# Получаем результат выполнения запроса
result = cursor.fetchall()

# Выводим результат
for row in result:
    print(row)

# Закрываем курсор и соединение с базой данных
cursor.close()
db.close()
