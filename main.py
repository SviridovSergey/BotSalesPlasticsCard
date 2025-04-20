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

#вид пластика:белый, серебрянный, золотой, прозрачный(стоимость 1 карты от кол-ва), добавить нужен ли 
# дизайн макета(+ к стоимости)
#сначало выбирается пластик и потом идет по кол-ву(от 100 до 200 и тд), потом до элементы(qr code и тд)
#общ стоимость считать
# Структура данных с ценами
prices = {
    "от 100 до 200 карточек": {
        "Белый": 19.50,
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
        "Тиснение (фальгирование)": 0,
        "Скретч-полосса (стираемый слой)": 0,
        "Полоса для подписи": 0
    },
    "от 200 до 300 карточек": {
        "Белый": 19.00,
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
        "Тиснение (фальгирование)": 0,
        "Скретч-полосса (стираемый слой)": 0,
        "Полоса для подписи": 0
    },
    "от 300 до 500 карточек": {
        "Белый": 18.00,
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
        "Тиснение (фальгирование)": 0,
        "Скретч-полосса (стираемый слой)": 0,
        "Полоса для подписи": 0
    },
    "от 500 до 700 карточек": {
        "Белый": 17.00,
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
        "Тиснение (фальгирование)": 0,
        "Скретч-полосса (стираемый слой)": 0,
        "Полоса для подписи": 0
    },
    "от 700 до 1000 карточек": {
        "Белый": 15.00,
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
        "Тиснение (фальгирование)": 0,
        "Скретч-полосса (стираемый слой)": 0,
        "Полоса для подписи": 0
    },
    "от 1000 до 2000 карточек": {
        "Белый": 14.00,
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
        "Тиснение (фальгирование)": 0,
        "Скретч-полосса (стираемый слой)": 0,
        "Полоса для подписи": 0
    },
    "от 2000 до 3000 карточек": {
        "Белый": 12.00,
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
        "Тиснение (фальгирование)": 0,
        "Скретч-полосса (стираемый слой)": 0,
        "Полоса для подписи": 0
    },
    "от 3000 до 5000 карточек": {
        "Белый": 0,
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
        "Тиснение (фальгирование)": 0,
        "Скретч-полосса (стираемый слой)": 0,
        "Полоса для подписи": 0
    },
    "от 5000 до 10000 карточек": {
        "Белый": 0,
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
        "Тиснение (фальгирование)": 0,
        "Скретч-полосса (стираемый слой)": 0,
        "Полоса для подписи": 0
    }
}

chip_prices={
    "Em-Marine" : {
        "от 10 до 100" : 45.00,
        "от 101 до 500" : 36.00,
        "от 501 до 1100" : 33.00,
        "от 1101 до 3000" : 30.00,
        "от 3001 до 5000" : 29.00,
        "от 5001 до 10000" : 0
    },
    "Mifare" : {
        "от 10 до 100" : 46.00,
        "от 101 до 500" : 37.00,
        "от 501 до 1100" : 34.00,
        "от 1101 до 3000" : 31.00,
        "от 3001 до 5000" : 28.00,
        "от 5001 до 10000" : 0
    }
}

# Клавиатура для команды /start
markup_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
button2 = types.KeyboardButton("от 100 до 200 карточек")
button3 = types.KeyboardButton("от 200 до 300 карточек")
button4 = types.KeyboardButton("от 500 до 700 карточек")
button5 = types.KeyboardButton("от 700 до 1000 карточек")
button6 = types.KeyboardButton("ОТ 1000 ДО 2000 карточек")
button7 = types.KeyboardButton("от 2000 до 3000 карточек")
button8 = types.KeyboardButton("от 3000 до 5000 карточек")
button9 = types.KeyboardButton("от 5000 до 10000 карточек")
logging.info("Buttons command start are initialized")

markup_start.add(button2, button3, button4, button5, button6, button7, button8, button9)
logging.info("Buttons are pushed to telegram(start)")

# Клавиатура для команды /pers
markup_pers = types.ReplyKeyboardMarkup(resize_keyboard=True)
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
button23 = types.KeyboardButton("Готово")
logging.info("Buttons command pers are initialized")

markup_pers.add(button13, button14, button15, button16, button17,
                 button18, button19, button20, button21, button22,button23)
logging.info("Buttons are pushed  to telegram(pers)")

#кнопки для выбора типа чипа
markup_chip_type=types.ReplyKeyboardMarkup(resize_keyboard=True)
button_chip_em_marine=types.KeyboardButton("Em-Marine")
button_chip_mifare=types.KeyboardButton("Mifare")
logging.info("Buttons command chipcards are initialized")

markup_chip_type.add(button_chip_em_marine,button_chip_mifare)
logging.info("Buttons are pushed  to telegram(chipcards)")

#клавиатура для выбора кол-ва карт с чипами
markup_chip_quantity=types.ReplyKeyboardMarkup(resize_keyboard=True)
button_chip_10_10=types.KeyboardButton("от 10 до 100")
button_chip_101_500=types.KeyboardButton("от 101 до 500")
button_chip_501_1100=types.KeyboardButton("от 501 до 1100")
button_chip_1101_3000=types.KeyboardButton("от 1101 до 3000")
button_chip_3001_5000=types.KeyboardButton("от 3001 до 5000")
button_chip_5001_10000=types.KeyboardButton("от 5001 до 10000")
logging.info("Buttons command chipcards are initialized")

markup_chip_quantity.add(button_chip_10_10,button_chip_101_500,button_chip_1101_3000,
                  button_chip_3001_5000, button_chip_5001_10000)
logging.info("Buttons are pushed  to telegram(chipcards)")

markup_plastic=types.ReplyKeyboardMarkup(resize_keyboard=True)
button_plastic_1=types.KeyboardButton("Белый")
button_plastic_2=types.KeyboardButton("Золото")
button_plastic_3=types.KeyboardButton("Серебро")
button_plastic_4=types.KeyboardButton("Прозрачный")
logging.info("Buttons for choise of plastic are initialized")

markup_plastic.add(button_plastic_1,button_plastic_2,button_plastic_3,button_plastic_4)
logging.info("Buttons are pushed  to telegram(choise of plastic)")

# Обработчик команды /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    chat_id = message.chat.id
    if chat_id not in user_state:
        user_state[chat_id] = {}
    user_state[chat_id]["quantity"] = None
    user_state[chat_id]["plastic"] = None
    user_state[chat_id]["extras"] = []  # Используем правильный ключ "extras"
    bot.reply_to(
        message,
        "Выберите количество карточек:",
        reply_markup=markup_start,
    )
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
def handle_quantity(message):
    chat_id = message.chat.id
    if chat_id not in user_state:
        user_state[chat_id] = {}
    user_state[chat_id]["quantity"] = message.text
    bot.send_message(
        chat_id,
        "Теперь выберите тип пластика:",
        reply_markup=markup_plastic,
    )
    logging.info(f"User {chat_id} selected quantity: {message.text}")

#обработчик выбора пластика
@bot.message_handler(func=lambda message: message.text in [
    "Белый",
    "Золото",
    "Серебряно",
    "Прозрачный"
])
def handle_plastic(message):
    chat_id = message.chat.id
    if chat_id not in user_state:
        user_state[chat_id] = {}  # Инициализация, если пользователь отсутствует
    user_state[chat_id]["plastic"] = message.text
    bot.send_message(
        chat_id,
        "Хотите добавить дополнительные элементы? Выберите или нажмите 'Готово':",
        reply_markup=markup_pers,
    )
    logging.info(f"User {chat_id} selected plastic: {message.text}")

#обработчик команы /chipcards
@bot.message_handler(commands=["chipcards"])
def chipcards(message):
    chat_id = message.chat.id
    if chat_id not in user_state:
        user_state[chat_id] = {}
    user_state[chat_id]["chip_type"] = None
    user_state[chat_id]["chip_quantity"] = None
    bot.send_message(chat_id, "Выберите тип чипа:", reply_markup=markup_chip_type)
    logging.info("Command /chipcards executed")

#обработчик выбора типа чипа
@bot.message_handler(func=lambda message: message.text in ["Em-Marine", "Mifare"])
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
    state = user_state.get(chat_id)
    if not state or not state["chip_type"] or not state["chip_quantity"]:
        bot.send_message(chat_id, "Необходимо выбрать тип чипа и количество карт.")
        return
    chip_type = state["chip_type"]
    chip_quantity = state["chip_quantity"]
    price = chip_prices.get(chip_type, {}).get(chip_quantity, "Неизвестный диапазон")
    if isinstance(price, str):
        bot.send_message(chat_id, f"Для выбранного типа чипа ({chip_type}) и количества карт ({chip_quantity}) цена не определена.")
        return
    bot.send_message(chat_id, f"Стоимость карт с чипом {chip_type} ({chip_quantity}): {price} Р")
    logging.info(f"User {chat_id} calculated chip card cost: {price}")

# Обработчик команды /pers
@bot.message_handler(commands=["pers"])
def pers(message):
    chat_id = message.chat.id
    # Проверка и инициализация ключа extras, если его нет
    if chat_id not in user_state:
        user_state[chat_id] = {}
    if "extras" not in user_state[chat_id]:
        user_state[chat_id]["extras"] = []
    bot.send_message(chat_id, "Выберите дополнительный материал:", reply_markup=markup_pers)
    logging.info("Command /pers executed")

# Обработчик текстовых сообщений для команды /pers
@bot.message_handler(func=lambda message: message.text in [
    "Штрих-код",
    "Магнитная полоса с кодированием",
    "Печатный номер",
    "Отверстия в карте (за каждое)",
    "Магнитный винил (Магниты)",
    "Фактурное покрытие",
    "Эмбоссирование и типирование",
    "Тиснение (фальгирование)",
    "Скретч-полосса (стираемый слой)",
    "Полоса для подписи",
    "Готово"
])
def handle_pers_buttons(message):
    chat_id = message.chat.id
    # Проверка и инициализация ключа extras, если его нет
    if chat_id not in user_state:
        user_state[chat_id] = {}
    if "extras" not in user_state[chat_id]:
        user_state[chat_id]["extras"] = []

    if message.text == "Готово":
        calculate_cost(chat_id)
        return
    if message.text not in user_state[chat_id]["extras"]:
        user_state[chat_id]["extras"].append(message.text)
        bot.send_message(chat_id, f"Добавлен элемент: {message.text}. Выберите еще или нажмите 'Готово'.",
                         reply_markup=markup_pers)
    else:
        bot.send_message(chat_id, f"Элемент '{message.text}' уже добавлен")

# Обработчик команды /calculate
@bot.message_handler(commands=["calculate"])
def calculate_cost(chat_id):
    state = user_state.get(chat_id)
    if not state or not state["quantity"] or not state["plastic"]:
        bot.send_message(chat_id, "Вы не выбрали все параметры. Попробуйте снова.")
        return

    # Базовая стоимость пластика
    base_price = prices[state["quantity"]][state["plastic"]]
    total_cost = base_price

    # Добавляем стоимость дополнительных элементов
    for extra in state["extras"]:
        extra_price = prices[state["quantity"]].get(extra, 0)
        if isinstance(extra_price, str):
            bot.send_message(chat_id, f"Элемент '{extra}' не имеет фиксированной цены.")
            continue
        total_cost += extra_price

    # Отправляем итоговую стоимость
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