import logging
import telebot
import os
import time
import re
import threading
from contextlib import contextmanager
from telebot import types
from PIL import Image,ImageDraw,ImageFont

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

BASE_IMAGE_DIR = "C:\\Users\\abcda\\vscode\\fulprojects\\tgbot\\image"
MAX_FILE_AGE=10
TEMP_FILE_PATTERN=re.compile(r"^\d+_\w+\.png$")  # Например: 1231091537_card.png)

if not os.path.exists(BASE_IMAGE_DIR):
    os.makedirs("image")

base_image = {
    "Белый": os.path.join(BASE_IMAGE_DIR, "white_base.jpg"),
    "Золото": os.path.join(BASE_IMAGE_DIR, "gold_base.jpg"),
    "Серебро": os.path.join(BASE_IMAGE_DIR, "silver_base.jpg"),
    "Прозрачный": os.path.join(BASE_IMAGE_DIR, "transparent_base.jpg")
}

extra_icons = {
    "Штрих-код": os.path.join(BASE_IMAGE_DIR, "barcode.png"),
    "Магнитная полоса с кодированием": os.path.join(BASE_IMAGE_DIR, "magnetic_strip.png"),
    "Печатный номер": os.path.join(BASE_IMAGE_DIR, "print_number.png"),
    "Отверстия в карте (за каждое)": os.path.join(BASE_IMAGE_DIR, "hole.png"),
    "Магнитный винил (Магниты)": os.path.join(BASE_IMAGE_DIR, "magnetic_vinyl.png"),
    "Фактурное покрытие": os.path.join(BASE_IMAGE_DIR, "texture.png"),
    "Эмбоссирование и типирование": os.path.join(BASE_IMAGE_DIR, "emboss.png"),
    "Тиснение (фальгирование)": os.path.join(BASE_IMAGE_DIR, "foil.png"),
    "Скретч-полосса (стираемый слой)": os.path.join(BASE_IMAGE_DIR, "scratch.png"),
    "Полоса для подписи": os.path.join(BASE_IMAGE_DIR, "signature.png")
}

def periodic_cleanup():
    while True:
        try:
            cleanup_temp_file()
            time.sleep(10)
        except Exception as e:
            logging.error(f"Error during periodic cleanup: {e}")

@contextmanager
def temporary_file(path):
    try:
        yield path
    finally:
        if os.path.exists(path) and TEMP_FILE_PATTERN.match(os.path.basename(path)):
            try:
                os.remove()
                logging.info(f"Auto-deleted temporary file: {path}")
            except Exception as e:
                logging.error(f"Error auto-deleting file {path} : {e}")

def cleanup_temp_file():
    current_time=time.time()
    for filename in os.listdir("image"):
        file_path=os.path.join("image",filename)

        if os.path.isfile(file_path) and TEMP_FILE_PATTERN.match(filename):
            if (current_time - os.path.getctime(file_path)) > MAX_FILE_AGE:
                try:
                    os.remove(file_path)
                    logging.info(f"Deleted temporary file : {file_path}")
                except Exception as e:
                    logging.error(f"Error deleting file {file_path} : {e}")


def create_placeholder(color, size = (600,400)):
    image=Image.new("RGBA", size,color)
    draw=ImageDraw.Draw(image)
    draw.rectangle([10,10,size[0]-10, size[1]-10], outline="black", width=2)
    return image

def create_card_image(chat_id):
    state = user_state.get(chat_id)
    # Создаем новое изображение на основе выбранного пластика
    base_image_path = base_image.get(state["plastic"])
    
    # Проверяем существование файла
    if not base_image_path or not os.path.exists(base_image_path):
        logging.error(f"Base image for plastic '{state['plastic']}' not found")
        if state["plastic"]=="Блеый":
            card_image=create_placeholder((255,255,255))
        elif state["plastic"]=="Золото":
            card_image=create_placeholder((212,175,55))
        elif state["plastic"]=="Серербро":
            card_image=create_placeholder((192,192,192))
        elif state["plastic"]=="Прозрачный":
            card_image=create_placeholder((200,200,200,128))
        else:
            card_image=create_placeholder((255,255,255))
    else:
        card_image=Image.open(base_image_path).convert("RGBA")
    
    card_image = Image.open(base_image_path).convert("RGBA")
    draw = ImageDraw.Draw(card_image)
    
    # Добавляем дополнительные параметры
    y_offset = 50
    for extra in state["extras"]:
        icon_path = extra_icons.get(extra)
        if icon_path and os.path.exists(icon_path):
            icon = Image.open(icon_path).convert("RGBA")
            card_image.paste(icon, (50, y_offset), icon)
            y_offset += 50
    
    result_path = f'image/{chat_id}_card.png'
    card_image.save(result_path)
    return result_path


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
    "Серебро",
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
    
    base_price = prices[state["quantity"]][state["plastic"]]
    total_cost = base_price
    
    for extra in state["extras"]:
        extra_price = prices[state["quantity"]].get(extra, 0)
        if isinstance(extra_price, str):
            bot.send_message(chat_id, f"Элемент '{extra}' не имеет фиксированной цены.")
            continue
        total_cost += extra_price
    
    try:
        image_path = create_card_image(chat_id)
        with temporary_file(image_path) as photo_path:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo, caption=f"Итоговая стоимость: {total_cost} Р")
    except Exception as e:
        logging.error(f"Error creating image: {e}")
        bot.send_message(chat_id, f"Итоговая стоимость: {total_cost} Р")
    
    logging.info(f"User {chat_id} calculated total cost: {total_cost}")

# Обработчик ошибок
@bot.message_handler(func=lambda message: True)
def handle_error(message):
    bot.reply_to(message, "Неизвестная команда. Пожалуйста, используйте кнопки.")
    logging.error(f"Unknown command received: {message.text}")

cleanup_thread=threading.Thread(target=periodic_cleanup,daemon=True)
cleanup_thread.start()

# Основная функция запуска бота
def main() -> None:
    # Удаляем вебхук
    bot.remove_webhook()
    logger.info("Webhook removed")

    # Запускаем polling
    logger.info("Bot started with polling")
    cleanup_temp_file()
    bot.polling()

if __name__ == "__main__":
    main()