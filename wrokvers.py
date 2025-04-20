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
    "от 100 до 200 карточек": {
        "Белый": 19.50,
        "Золотой": 22.00,
        "Серебряный": 21.00,
        "Прозрачный": 25.00,
        "Штрих-код": 0.50,
        "Магнитная полоса с кодированием": 3.50,
        "Печатный номер": 0.50,
    },
    # Добавьте остальные диапазоны аналогично...
}

# Клавиатура для выбора количества карточек
markup_quantity = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons_quantity = [
    "от 100 до 200 карточек",
    "от 200 до 300 карточек",
    "от 300 до 500 карточек",
    "от 500 до 700 карточек",
    "от 700 до 1000 карточек",
    "от 1000 до 2000 карточек",
]
for button in buttons_quantity:
    markup_quantity.add(types.KeyboardButton(button))

# Клавиатура для выбора пластика
markup_plastic = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons_plastic = ["Белый", "Золотой", "Серебряный", "Прозрачный"]
for button in buttons_plastic:
    markup_plastic.add(types.KeyboardButton(button))

# Клавиатура для дополнительных элементов
markup_extras = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons_extras = ["Штрих-код", "Магнитная полоса с кодированием", "Печатный номер", "Готово"]
for button in buttons_extras:
    markup_extras.add(types.KeyboardButton(button))

# Обработчик команды /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    chat_id = message.chat.id
    if chat_id not in user_state:
        user_state[chat_id] = {}
    user_state[chat_id]["quantity"] = None
    user_state[chat_id]["plastic"] = None
    user_state[chat_id]["extras"] = []
    bot.reply_to(
        message,
        "Выберите количество карточек:",
        reply_markup=markup_quantity,
    )
    logging.info("Command /start executed")

# Обработчик выбора количества карточек
@bot.message_handler(func=lambda message: message.text in buttons_quantity)
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

# Обработчик выбора пластика
@bot.message_handler(func=lambda message: message.text in buttons_plastic)
def handle_plastic(message):
    chat_id = message.chat.id
    if chat_id not in user_state:
        user_state[chat_id] = {}
    user_state[chat_id]["plastic"] = message.text
    bot.send_message(
        chat_id,
        "Хотите добавить дополнительные элементы? Выберите или нажмите 'Готово':",
        reply_markup=markup_extras,
    )
    logging.info(f"User {chat_id} selected plastic: {message.text}")

# Обработчик выбора дополнительных элементов
@bot.message_handler(func=lambda message: message.text in buttons_extras)
def handle_extras(message):
    chat_id = message.chat.id
    if message.text == "Готово":
        calculate_cost(chat_id)
        return
    if message.text not in user_state[chat_id]["extras"]:
        user_state[chat_id]["extras"].append(message.text)
        bot.send_message(
            chat_id,
            f"Добавлен элемент: {message.text}. Выберите ещё или нажмите 'Готово'.",
            reply_markup=markup_extras,
        )
    else:
        bot.send_message(chat_id, f"Элемент '{message.text}' уже добавлен.")

# Расчет итоговой стоимости
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
    bot.remove_webhook()
    logger.info("Webhook removed")
    logger.info("Bot started with polling")
    bot.polling()

if __name__ == "__main__":
    main()