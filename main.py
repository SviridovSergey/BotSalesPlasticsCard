import logging
import telebot
from telebot import types

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота
TOKEN = "8086181539:AAG8tdzVKEQONpcb9F8tldJiKaXxu9nypGs"
bot = telebot.TeleBot(TOKEN)

# Глобальный словарь для хранения состояния пользователей
user_state = {}

# Структура данных с ценами
prices = {
    "до 100 карточек": {
        "Белый (4+4)": 20.00,
        "Серебро": 3.50,
        "Золото": 3.50,
        "Прозрачный": 6.50,
        "Штрих-код": 0.50,
        "Магнитная полоса с кодированием": 3.50,
        "Печатный номер": 0.50,
        "Отверстия в карте (за каждое)": 0.50,
        "Магнитный винил (Магниты)": 3.50,
        "Фактурное покрытие": 2.00,
        "Эмбоссирование и типирование": 3.50,
        "Тиснение (фальгирование)": "Индивидуально",
        "Скретч-полосса (стираемый слой)": "Индивидуально",
        "Полоса для подписи": "Индивидуально",
        "EM-Marine": 45.00,
        "Mifare": 46.00
    },
    "от 100 до 200 карточек": {
        "Белый (4+4)": 19.50,
        "Серебро": 3.50,
        "Золото": 3.50,
        "Прозрачный": 6.50,
        "Штрих-код": 0.50,
        "Магнитная полоса с кодированием": 3.50,
        "Печатный номер": 0.50,
        "Отверстия в карте (за каждое)": 0.50,
        "Магнитный винил (Магниты)": 3.50,
        "Фактурное покрытие": 2.00,
        "Эмбоссирование и типирование": 3.50,
        "Тиснение (фальгирование)": "Индивидуально",
        "Скретч-полосса (стираемый слой)": "Индивидуально",
        "Полоса для подписи": "Индивидуально",
        "Em-Marine": 36.00,
        "Mifare": 37.00
    },
    "от 200 до 300 карточек": {
        "Белый (4+4)": 19.00,
        "Серебро": 3.50,
        "Золото": 3.50,
        "Прозрачный": 6.50,
        "Штрих-код": 0.50,
        "Магнитная полоса с кодированием": 3.50,
        "Печатный номер": 0.50,
        "Отверстия в карте (за каждое)": 0.50,
        "Магнитный винил (Магниты)": 3.50,
        "Фактурное покрытие": 2.00,
        "Эмбоссирование и типирование": 3.50,
        "Тиснение (фальгирование)": "Индивидуально",
        "Скретч-полосса (стираемый слой)": "Индивидуально",
        "Полоса для подписи": "Индивидуально",
    },
    "от 300 до 500 карточек": {
        "Белый (4+4)": 18.00,
        "Серебро": 3.50,
        "Золото": 3.50,
        "Прозрачный": 6.50,
        "Штрих-код": 0.50,
        "Магнитная полоса с кодированием": 3.50,
        "Печатный номер": 0.50,
        "Отверстия в карте (за каждое)": 0.50,
        "Магнитный винил (Магниты)": 3.50,
        "Фактурное покрытие": 2.00,
        "Эмбоссирование и типирование": 3.50,
        "Тиснение (фальгирование)": "Индивидуально",
        "Скретч-полосса (стираемый слой)": "Индивидуально",
        "Полоса для подписи": "Индивидуально",
    },
    "от 500 до 700 карточек": {
        "Белый (4+4)": 17.00,
        "Серебро": 3.50,
        "Золото": 3.50,
        "Прозрачный": 6.50,
        "Штрих-код": 0.50,
        "Магнитная полоса с кодированием": 3.50,
        "Печатный номер": 0.50,
        "Отверстия в карте (за каждое)": 0.50,
        "Магнитный винил (Магниты)": 3.50,
        "Фактурное покрытие": 2.00,
        "Эмбоссирование и типирование": 3.50,
        "Тиснение (фальгирование)": "Индивидуально",
        "Скретч-полосса (стираемый слой)": "Индивидуально",
        "Полоса для подписи": "Индивидуально",
    },
    "от 700 до 1000 карточек": {
        "Белый (4+4)": 15.00,
        "Серебро": 3.50,
        "Золото": 3.50,
        "Прозрачный": 6.50,
        "Штрих-код": 0.50,
        "Магнитная полоса с кодированием": 3.50,
        "Печатный номер": 0.50,
        "Отверстия в карте (за каждое)": 0.50,
        "Магнитный винил (Магниты)": 3.50,
        "Фактурное покрытие": 2.00,
        "Эмбоссирование и типирование": 3.50,
        "Тиснение (фальгирование)": "Индивидуально",
        "Скретч-полосса (стираемый слой)": "Индивидуально",
        "Полоса для подписи": "Индивидуально",
    },
    "от 1000 до 2000 карточек": {
        "Белый (4+4)": 14.00,
        "Серебро": 3.50,
        "Золото": 3.50,
        "Прозрачный": 6.50,
        "Штрих-код": 0.50,
        "Магнитная полоса с кодированием": 3.50,
        "Печатный номер": 0.50,
        "Отверстия в карте (за каждое)": 0.50,
        "Магнитный винил (Магниты)": 3.50,
        "Фактурное покрытие": 2.00,
        "Эмбоссирование и типирование": 3.50,
        "Тиснение (фальгирование)": "Индивидуально",
        "Скретч-полосса (стираемый слой)": "Индивидуально",
        "Полоса для подписи": "Индивидуально",
    },
    "от 2000 до 3000 карточек": {
        "Белый (4+4)": 12.00,
        "Серебро": 3.50,
        "Золото": 3.50,
        "Прозрачный": 6.50,
        "Штрих-код": 0.50,
        "Магнитная полоса с кодированием": 3.50,
        "Печатный номер": 0.50,
        "Отверстия в карте (за каждое)": 0.50,
        "Магнитный винил (Магниты)": 3.50,
        "Фактурное покрытие": 2.00,
        "Эмбоссирование и типирование": 3.50,
        "Тиснение (фальгирование)": "Индивидуально",
        "Скретч-полосса (стираемый слой)": "Индивидуально",
        "Полоса для подписи": "Индивидуально",
    },
    "от 3000 до 5000 карточек": {
        "Белый (4+4)": "Индивидуально",
        "Серебро": 3.50,
        "Золото": 3.50,
        "Прозрачный": 6.50,
        "Штрих-код": 0.50,
        "Магнитная полоса с кодированием": 3.50,
        "Печатный номер": 0.50,
        "Отверстия в карте (за каждое)": 0.50,
        "Магнитный винил (Магниты)": 3.50,
        "Фактурное покрытие": 2.00,
        "Эмбоссирование и типирование": 3.50,
        "Тиснение (фальгирование)": "Индивидуально",
        "Скретч-полосса (стираемый слой)": "Индивидуально",
        "Полоса для подписи": "Индивидуально",
    },
    "от 5000 до 10000 карточек": {
        "Белый (4+4)": "Индивидуально",
        "Серебро": 3.50,
        "Золото": 3.50,
        "Прозрачный": 6.50,
        "Штрих-код": 0.50,
        "Магнитная полоса с кодированием": 3.50,
        "Печатный номер": 0.50,
        "Отверстия в карте (за каждое)": 0.50,
        "Магнитный винил (Магниты)": 3.50,
        "Фактурное покрытие": 2.00,
        "Эмбоссирование и типирование": 3.50,
        "Тиснение (фальгирование)": "Индивидуально",
        "Скретч-полосса (стираемый слой)": "Индивидуально",
        "Полоса для подписи": "Индивидуально",
    }
}

chip_prices={
    "Em-Marine" : {
        "от 10 до 100" : 45.00,
        "от 101 до 500" : 36.00,
        "от 501 до 1100" : 33.00,
        "от 1101 до 3000" : 30.00,
        "от 3001 до 5000" : 29.00,
        "от 5001 до 10000" : "Индидуально"
    },
    "Mifare" : {
        "от 10 до 100" : 46.00,
        "от 101 до 500" : 37.00,
        "от 501 до 1100" : 34.00,
        "от 1101 до 3000" : 31.00,
        "от 3001 до 5000" : 28.00,
        "от 5001 до 10000" : "ИндивидуальноЫ"
    }
}

# Клавиатура для команды /start
markup_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = types.KeyboardButton("до 100 карточек")
button2 = types.KeyboardButton("от 100 до 200 карточек")
button3 = types.KeyboardButton("от 200 до 300 карточек")
button4 = types.KeyboardButton("от 500 до 700 карточек")
button5 = types.KeyboardButton("от 700 до 1000 карточек")
button6 = types.KeyboardButton("ОТ 1000 ДО 2000 карточек")
button7 = types.KeyboardButton("от 2000 до 3000 карточек")
button8 = types.KeyboardButton("от 3000 до 5000 карточек")
button9 = types.KeyboardButton("от 5000 до 10000 карточек")
markup_start.add(button1, button2, button3, button4, button5, button6, button7, button8, button9)
logging.info("Buttons command start are initialized ")

# Клавиатура для команды /pers
markup_pers = types.ReplyKeyboardMarkup(resize_keyboard=True)
button10 = types.KeyboardButton("Серебро")
button11 = types.KeyboardButton("Золото")
button12 = types.KeyboardButton("Прозрачный")
button13 = types.KeyboardButton("Штрих-код")
button14 = types.KeyboardButton("Магнитная полоса с кодированием")
button15 = types.KeyboardButton("Печатный номер")
button16 = types.KeyboardButton("Отверстия в карте (за каждое)")
button17 = types.KeyboardButton("Магнитный винил (Магниты)")
button18 = types.KeyboardButton("Фактурное покрытие")
button19 = types.KeyboardButton("Эмбоссирование и типирование")
button20 = types.KeyboardButton("Тиснение (фальгирование)")
button21 = types.KeyboardButton("Скретч-полосса (стираемый слой)")
button22 = types.KeyboardButton("Полоса для подписи")
markup_pers.add(button10, button11, button12, button13, button14, button15, button16, button17, button18, button19, button20, button21, button22)
logging.info("Buttons command pers are initialized")

#кнопки для выбора типа чипа
markup_chip_type=types.ReplyKeyboardMarkup(resize_keyboard=True)
button_chip_em_marine=types.KeyboardButton("Em-Marine")
button_chip_mifare=types.KeyboardButton("Mifare")
markup_chip_type.add(button_chip_em_marine,button_chip_mifare)
logging.info("Main Buttons aommand chicards are initialized")

#клавиатура для выбора кол-ва карт с чипами
markup_chip_quantity=types.ReplyKeyboardMarkup(resize_keyboard=True)
button_chip_10_10=types.KeyboardButton("от 10 до 100")
button_chip_101_500=types.KeyboardButton("от 101 до 500")
button_chip_501_1100=types.KeyboardButton("от 501 до 1100")
button_chip_1101_3000=types.KeyboardButton("от 1101 до 3000")
button_chip_3001_5000=types.KeyboardButton("от 3001 до 5000")
button_chip_5001_10000=types.KeyboardButton("от 5001 до 10000")
markup_chip_quantity.add(button_chip_10_10,button_chip_101_500,button_chip_1101_3000,
                  button_chip_3001_5000, button_chip_5001_10000)
logging.info("Buttons command chipcards are initialized")


# Обработчик команды /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    chat_id = message.chat.id
    # Инициализируем состояние только если оно еще не создано
    if chat_id not in user_state:
        user_state[chat_id] = {}
    user_state[chat_id]["card_quantity"] = None
    user_state[chat_id]["materials"] = []
    bot.reply_to(message, "Выберите количество карточек из белого пластика (4+4) с помощью кнопок:", reply_markup=markup_start)
    logging.info("Command /start executed")

# Обработчик текстовых сообщений для команды /start
@bot.message_handler(func=lambda message: message.text in [
    "до 100 карточек",
    "от 100 до 200 карточек",
    "от 200 до 300 карточек",
    "от 500 до 700 карточек",
    "от 700 до 1000 карточек",
    "ОТ 1000 ДО 2000 карточек",
    "от 2000 до 3000 карточек",
    "от 3000 до 5000 карточек",
    "от 5000 до 10000 карточек"
])
def handle_start_buttons(message):
    chat_id = message.chat.id
    if chat_id not in user_state:
        user_state[chat_id] = {}
    user_state[chat_id]["card_quantity"] = message.text
    bot.send_message(chat_id, "Теперь выберите материалы и персонализацию:", reply_markup=markup_pers)
    logging.info(f"User {chat_id} selected quantity: {message.text}")

#обработчик команы /chipcards
@bot.message_handler(commands=["chipcards"])
def chipcards(message):
    chat_id = message.chat.id
    # Инициализируем состояние только если оно еще не создано
    if chat_id not in user_state:
        user_state[chat_id] = {}
    user_state[chat_id]["chip_type"] = None
    user_state[chat_id]["chip_quantity"] = None
    bot.send_message(chat_id, "Выберите тип чипа:", reply_markup=markup_chip_type)
    logging.info("Command /chipcards executed")

#обработчик выбора типа чипа
@bot.message_handler(func=lambda message: message.text in ["EM-Marine", "Mifare"])
def handle_chip_type(message):
    chat_id = message.chat.id
    if chat_id not in user_state:
        user_state[chat_id] = {}
    user_state[chat_id]["chip_type"] = message.text
    bot.send_message(chat_id, "Теперь выберите количество карт с чипами:", reply_markup=markup_chip_quantity)
    logging.info(f"User {chat_id} selected chip type: {message.text}")

#обработчик выбора кол-ва карт с чипами    
@bot.message_handler(func=lambda message: message.text in [
    "от 10 до 100",
    "от 101 до 500",
    "от 501 до 1100",
    "от 1101 до 3000",
    "от 3000 до 5000",
    "от 5001 до 10000"
])

def handle_chip_quantity(message):
    chat_id = message.chat.id
    if chat_id not in user_state or not user_state[chat_id].get("chip_type"):
        bot.send_message(chat_id, "Сначала выберите тип чипа.")
        return
    user_state[chat_id]["chip_quantity"] = message.text
    bot.send_message(chat_id, f"Вы выбрали {message.text} карт с чипом {user_state[chat_id]['chip_type']}.")
    calculate_chip_cost(chat_id)

def calculate_chip_cost(chat_id):
    state=user_state.get(chat_id)
    if not state or not state["chip_type"] or not state["chip_quantity"]:
        bot.send_message(chat_id, "Необходимо выбрать тип чипа и количество карт.")
        return
    
    chip_type=state["chip_type"]
    chip_quantity=state["chip_quantity"]
    
    price=chip_prices.get(chip_type, {}).get(chip_quantity, "Неизвестный диапозон")
    if isinstance(price, str):
        bot.send_message(chat_id, f"Для выбранного чипа типа ({chip_type})",
                          "и количество карт ({chip_quantity}) не определена")
        return
    bot.send_message(chat_id,f"Стоимость карт с чипом {chip_type} ({chip_quantity}) : {price}Р")
    logging.info(f"User {chat_id} calculated chip card cost : {price}")
# Обработчик команды /pers
@bot.message_handler(commands=["pers"])
def pers(message):
    bot.send_message(message.chat.id, "Выберите материал и персонализацию:", reply_markup=markup_pers)
    logging.info("Command /pers executed")

# Обработчик текстовых сообщений для команды /pers
@bot.message_handler(func=lambda message: message.text in [
    "Серебро",
    "Золото",
    "Прозрачный",
    "Штрих-код",
    "Магнитная полоса с кодированием",
    "Печатный номер",
    "Отверстия в карте (за каждое)",
    "Магнитный винил (Магниты)",
    "Фактурное покрытие",
    "Эмбоссирование и типирование",
    "Тиснение (фальгирование)",
    "Скретч-полосса (стираемый слой)",
    "Полоса для подписи"
])
def handle_pers_buttons(message):
    chat_id = message.chat.id
    if user_state.get(chat_id, {}).get("quantity"):
        user_state[chat_id]["materials"].append(message.text)
        bot.send_message(chat_id, f"Добавлен материал: {message.text}. Выберите ещё или нажмите /calculate для подсчета стоимости.")
    else:
        bot.send_message(chat_id, "Сначала выберите количество карточек.")

# Обработчик команды /calculate
@bot.message_handler(commands=["calculate"])
def calculate_cost(message):
    chat_id = message.chat.id
    state = user_state.get(chat_id)
    if not state or not state["quantity"] or not state["materials"]:
        bot.send_message(chat_id, "Вы не выбрали достаточное количество параметров. Попробуйте снова.")
        return

    total_cost = prices[state["quantity"]]["Белый (4+4)"]
    for material in state["materials"]:
        price = prices[state["quantity"]].get(material, "Неизвестный материал")
        if isinstance(price, str):
            bot.send_message(chat_id, f"Материал '{material}' не имеет фиксированной цены.")
            continue
        total_cost += price

    bot.send_message(chat_id, f"Итоговая стоимость: {total_cost} Р")
    logging.info(f"User {chat_id} calculated total cost: {total_cost}")

# Обработчик ошибок
@bot.message_handler(func=lambda message: True)
def handle_error(message):
    bot.reply_to(message, "Неизвестная команда. Пожалуйста, используйте кнопки.")
    logging.error(f"Unknown command received: {message.text}")

# Основная функция запуска бота
def main() -> None:
    # Удаляем вебхук
    bot.remove_webhook()
    logger.info("Webhook removed")

    # Запускаем polling
    logger.info("Bot started with polling")
    bot.polling()

if __name__ == "__main__":
    main()