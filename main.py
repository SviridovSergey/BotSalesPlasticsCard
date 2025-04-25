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
button6 = types.KeyboardButton("от 1000 до 2000 карточек")
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

BASE_IMAGE_DIR = "D:\\vscode\\BotSalesPlasticsCard\\image"
MAX_FILE_AGE=10
TEMP_FILE_PATTERN=re.compile(r"^\d+_\w+\.png$")  # Например: 1231091537_card.png)

# Размеры пластиковой карты (стандарт 86 мм × 54 мм)
card_width_mm = 86
card_height_mm = 54
pixel_per_mm = 3  # 1 мм = 3 пикселей
card_width_px = card_width_mm * pixel_per_mm
card_height_px = card_height_mm * pixel_per_mm

# Определяем границы карты
border_radius = 10 * pixel_per_mm  # Радиус закругления углов
logging.info("Constatns are initialized")
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
    "Фактурное покрытие": os.path.join(BASE_IMAGE_DIR, "texture.png"),
    "Эмбоссирование и типирование": os.path.join(BASE_IMAGE_DIR, "emboss.png"),
    #"Тиснение (фальгирование)": os.path.join(BASE_IMAGE_DIR, ""),
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
    if not state:
        raise ValueError("User state is missing")
    
    # Получаем путь к базовому изображению
    base_image_path = base_image.get(state["plastic"])
    if not base_image_path or not os.path.exists(base_image_path):
        logging.error(f"Base image for plastic '{state['plastic']}' not found")
        # Создаем placeholder, если базовое изображение не найдено
        color_map = {
            "Белый": (255, 255, 255),
            "Золото": (212, 175, 55),
            "Серебро": (192, 192, 192),
            "Прозрачный": (200, 200, 200, 128)
        }
        card_image = create_placeholder(color_map.get(state["plastic"], (255, 255, 255)))
    else:
        try:
            card_image = Image.open(base_image_path).convert("RGBA")
            card_image = card_image.resize((card_width_px, card_height_px), resample=Image.Resampling.LANCZOS)
        except Exception as e:
            logging.error(f"Error opening base image {base_image_path}: {e}")
            card_image = create_placeholder((255, 255, 255))
    
    draw = ImageDraw.Draw(card_image)
    
    # Определяем границы карты
    border_radius = 10 * pixel_per_mm  # Радиус закругления углов
    mask = Image.new('L', card_image.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle((0, 0, card_width_px - 1, card_height_px - 1), radius=border_radius, fill=255)
    # Применяем маску для закругления углов
    card_image.putalpha(mask)
    
    # Словарь с позициями для каждого элемента
    element_positions = {
        "Штрих-код": (card_width_px - 150, card_height_px - 150),  # Справа внизу
        "Магнитная полоса с кодированием": (0, card_height_px - 20),  # Внизу
        "Печатный номер": (50, card_height_px - 100),  # Под магнитной полосой
        "Отверстия в карте (за каждое)": (card_width_px - 150, card_height_px // 2),  # Справа по центру
        "Фактурное покрытие": (50, 50),  # Слева сверху
        "Эмбоссирование и типирование": (card_width_px // 2, 50),  # По центру сверху
        #"Тиснение (фальгирование)": (card_width_px // 2, card_height_px // 2),  # Центр
        "Скретч-полосса (стираемый слой)": (card_width_px - 150, 50),  # Справа сверху
    }
    
    # Размеры иконок
    icon_size = (100, 100)
    
    # Добавляем дополнительные элементы
    for extra in state["extras"]:
        icon_path = extra_icons.get(extra)
        if not icon_path or not os.path.exists(icon_path):
            logging.warning(f"Icon for extra '{extra}' not found")
            continue
        
        try:
            # Открываем иконку и масштабируем её
            icon = Image.open(icon_path).convert("RGBA")
            icon = icon.resize(icon_size)
            
            # Получаем позицию для текущего элемента
            position = element_positions.get(extra, (50, 50))  # По умолчанию (50, 50)
                        
            # Специфическая логика для элементов
            if extra == "Магнитная полоса с кодированием":
                magnetic_strip_path = extra_icons.get("Магнитная полоса с кодированием")
                if magnetic_strip_path and os.path.exists(magnetic_strip_path):
                    try:
                        # Открываем иконку магнитной полосы
                        magnetic_strip = Image.open(magnetic_strip_path).convert("RGBA")
                        # Масштабируем до нужных размеров (полная ширина карты × 20 пикселей)
                        magnetic_strip = magnetic_strip.resize((card_width_px, 20))
                        # Размещаем в нижней части карты
                        card_image.paste(magnetic_strip, (0, card_height_px - 20), magnetic_strip)
                    except Exception as e:
                        logging.error(f"Error processing magnetic strip: {e}")
                else:
                    # Если иконка не найдена, создаем черную полосу
                    magnetic_strip = Image.new("RGBA", (card_width_px, 20), color=(0, 0, 0, 255))
                    card_image.paste(magnetic_strip, (0, card_height_px - 20), magnetic_strip)
            
            elif extra == "Скретч-полосса (стираемый слой)":
                scratch_icon_path = extra_icons.get("Скретч-полосса (стираемый слой)")
                if scratch_icon_path and os.path.exists(scratch_icon_path):
                    try:
                        # Открываем иконку скретч-полосы
                        scratch_icon = Image.open(scratch_icon_path).convert("RGBA")
                        
                        # Масштабируем до нужных размеров
                        scratch_icon = scratch_icon.resize((150, 30))
                        
                        # Параметры размещения скретч-полоссы
                        horizontal_offset = 10  # Отступ от правого края
                        vertical_offset = 10   # Отступ от нижнего края
                        
                        # Позиция скретч-полоссы
                        scratch_position = (
                            card_width_px - scratch_icon.width - horizontal_offset,  # Горизонтальная позиция справа
                            card_height_px - scratch_icon.height - vertical_offset  # Вертикальная позиция снизу
                        )
                        
                        # Накладываем иконку скретч-полоссы
                        card_image.paste(scratch_icon, scratch_position, scratch_icon)
                    except Exception as e:
                        logging.error(f"Error processing scratch strip: {e}")
            
            elif extra == "Печатный номер":
                # Получаем путь к базовому изображению
                base_image_path = base_image.get(state["plastic"])
                if not base_image_path or not os.path.exists(base_image_path):
                    logging.error(f"Base image for plastic '{state['plastic']}' not found")
                    # Если базовое изображение не найдено, создаем placeholder
                    card_image = Image.new("RGBA", (card_width_px, card_height_px), color=(255, 255, 255))
                else:
                    try:
                        # Загружаем базовое изображение
                        card_image = Image.open(base_image_path).convert("RGBA")
                        card_image = card_image.resize((card_width_px, card_height_px), resample=Image.Resampling.LANCZOS)
                    except Exception as e:
                        logging.error(f"Error opening base image {base_image_path}: {e}")
                        # Если возникла ошибка при загрузке базового изображения, создаем placeholder
                        card_image = Image.new("RGBA", (card_width_px, card_height_px), color=(255, 255, 255))

                # Определяем границы карты
                border_radius = 10 * pixel_per_mm  # Радиус закругления углов
                mask = Image.new('L', card_image.size, 0)
                draw_mask = ImageDraw.Draw(mask)
                draw_mask.rounded_rectangle((0, 0, card_width_px - 1, card_height_px - 1), radius=border_radius, fill=255)
                # Применяем маску для закругления углов
                card_image.putalpha(mask)

                # Создаем объект для рисования
                draw = ImageDraw.Draw(card_image)

                # Логика для "Печатный номер"
                print_number_position = (50, 50)  # Позиция по умолчанию
                font = ImageFont.load_default()

                # Рисуем несколько прямоугольников с текстом
                num_rectangles = 4  # Четыре группы цифр
                rect_width = 50     # Ширина каждого прямоугольника
                rect_height = 20    # Высота каждого прямоугольника

                # Расчет начальной позиции
                start_x = print_number_position[0]
                start_y = print_number_position[1]

                # Рассчитываем интервал между прямоугольниками
                total_space = card_width_px - (num_rectangles * rect_width)
                spacing = total_space / (num_rectangles + 1)

                for i in range(num_rectangles):
                    rect_x = int(start_x + (i + 1) * spacing + i * rect_width)
                    rect_y = start_y
                    
                    # Проверяем, чтобы прямоугольник оставался на карте
                    if rect_x + rect_width > card_width_px:
                        break
                    
                    # Рисуем прямоугольник
                    draw.rectangle(
                        [
                            (rect_x, rect_y),
                            (rect_x + rect_width, rect_y + rect_height)
                        ],
                        outline="black",
                        width=2
                    )
                    
                    # Добавляем текст внутри прямоугольника
                    text = "xxxx"  # Текст внутри прямоугольника
                    text_bbox = draw.textbbox((rect_x, rect_y), text, font=font)
                    draw.text(
                        (
                            rect_x + (rect_width - font.getlength(text)) / 2,  # Выравнивание по центру
                            rect_y + 5
                        ),
                        text,
                        fill="black",  # Черный цвет текста
                        font=font
                    )
        
            elif extra == "Полоса для подписи":
                signature_strip_path = extra_icons.get("Полоса для подписи")
                if signature_strip_path and os.path.exists(signature_strip_path):
                    try:
                        # Открываем иконку полосы для подписи
                        signature_strip = Image.open(signature_strip_path).convert("RGBA")
                        
                        # Масштабируем до нужных размеров
                        signature_strip = signature_strip.resize((150, 30))
                        
                        # Параметры размещения полосы для подписи
                        horizontal_offset = 10  # Отступ от левого края
                        vertical_offset = 10   # Отступ от нижнего края
                        
                        # Позиция полосы для подписи
                        signature_position = (
                            horizontal_offset,  # Горизонтальная позиция слева
                            card_height_px // 2 - (signature_strip.height // 2)  # Вертикальная позиция по центру
                        )
                        
                        # Накладываем иконку полосы для подписи
                        card_image.paste(signature_strip, signature_position, signature_strip)
                    except Exception as e:
                        logging.error(f"Error processing signature strip: {e}")

            elif extra == "Штрих-код":

                # Получаем путь к базовому изображению
                base_image_path = base_image.get(state["plastic"])
                if not base_image_path or not os.path.exists(base_image_path):
                    logging.error(f"Base image for plastic '{state['plastic']}' not found")
                    # Если базовое изображение не найдено, создаем placeholder
                    card_image = Image.new("RGBA", (card_width_px, card_height_px), color=(255, 255, 255))
                else:
                    try:
                        # Загружаем базовое изображение
                        card_image = Image.open(base_image_path).convert("RGBA")
                        card_image = card_image.resize((card_width_px, card_height_px), resample=Image.Resampling.LANCZOS)
                    except Exception as e:
                        logging.error(f"Error opening base image {base_image_path}: {e}")
                        # Если возникла ошибка при загрузке базового изображения, создаем placeholder
                        card_image = Image.new("RGBA", (card_width_px, card_height_px), color=(255, 255, 255))

                # Определяем границы карты
                border_radius = 10 * pixel_per_mm  # Радиус закругления углов
                mask = Image.new('L', card_image.size, 0)
                draw_mask = ImageDraw.Draw(mask)
                draw_mask.rounded_rectangle((0, 0, card_width_px - 1, card_height_px - 1), radius=border_radius, fill=255)
                # Применяем маску для закругления углов
                card_image.putalpha(mask)

                # Создаем объект для рисования
                draw = ImageDraw.Draw(card_image)

                # Логика для штрих-кода
                barcode_icon_path = extra_icons.get("Штрих-код")
                if barcode_icon_path and os.path.exists(barcode_icon_path):
                    try:
                        # Открываем иконку штрих-кода
                        barcode_icon = Image.open(barcode_icon_path).convert("RGBA")
                        
                        # Масштабируем до нужных размеров
                        barcode_icon = barcode_icon.resize((150, 30))
                        
                        # Параметры размещения штрих-кода
                        horizontal_offset = 5  # Отступ от левого края
                        vertical_offset = 10   # Отступ от верхнего края
                        
                        # Позиция штрих-кода
                        barcode_position = (
                            horizontal_offset,  # Горизонтальная позиция слева
                            vertical_offset     # Вертикальная позиция сверху
                        )
                        
                        # Накладываем иконку штрих-кода
                        card_image.paste(barcode_icon, barcode_position, barcode_icon)
                    except Exception as e:
                        logging.error(f"Error processing barcode: {e}")
           
            # Проверяем, есть ли дополнение "Отверстия в карте (за каждое)"
            elif "Отверстия в карте (за каждое)" in state["extras"]:
                for extra in state["extras"]:
                    if extra == "Отверстия в карте (за каждое)":
                        hole_icon_path = extra_icons.get("Отверстия в карте (за каждое)")
                        if hole_icon_path and os.path.exists(hole_icon_path):
                            try:
                                # Открываем иконку отверстий
                                hole_icon = Image.open(hole_icon_path).convert("RGBA")
                                # Масштабируем до нужных размеров
                                hole_icon = hole_icon.resize((30, 30))
                                
                                # Параметры размещения отверстий
                                horizontal_offset = 10  # Отступ от левого края
                                card_center_y = card_height_px // 2  # Центральная часть карты по высоте
                                
                                # Позиция центрального отверстия
                                hole_position = (
                                    horizontal_offset,  # Фиксированный горизонтальный отступ
                                    card_center_y - (hole_icon.height // 2)  # Вертикальная позиция по центру
                                )
                                
                                # Накладываем иконку отверстия
                                card_image.paste(hole_icon, hole_position, hole_icon)
                            except Exception as e:
                                logging.error(f"Error processing holes: {e}")
                
            
        except Exception as e:
            logging.error(f"Error processing icon: {e}")

    # Сохраняем изображение
    result_path = os.path.join(BASE_IMAGE_DIR, f"{chat_id}_temp_card.png")
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
        user_state[chat_id]["extras"] = []
        logging.info("user-state params has initialized (Start)")

    # Путь к изображению
    photo_path = os.path.join(BASE_IMAGE_DIR, "startmessagecapction.jpg")

    # Короткая подпись для фото
    caption = "Добро пожаловать!"

    # Отправка фото с подписью
    with open(photo_path, 'rb') as photo_file:
        bot.send_photo(chat_id, photo_file, caption=caption, parse_mode='HTML')

    # Полный текст для отдельного сообщения
    full_text = (
        "Хотим представиться и познакомиться с вами!\n\n"
        "Мы являемся партнерами проверенного годами завода по\n"
        "производству пластиковых карт, и создали семейный\n"
        "бизнес для того, чтобы быть полезными и помогать Вам\n"
        "развивать свое дело, искать новую аудиторию и удерживать ее!\n"
        "Что в конечном итоге будет приводить к увеличению прибыли\n\n"
        "Мы компания по производству и поставке пластиковых карт, разработке\n"
        "Выпускаем:\n\n"
        "- Визитки на пластике для Ваших клиентов, которые цепляют внешним видом.\n"
        "- Дисконтные, бонусные, клубные карты\n"
        "- Изготовление бейджей, пропусков, ключей\n"
        "- Подарочные карты и сертификаты\n"
        "Наш сайт pink-card.ru\n\n"
        "<b> Этот бот поможет вам рассчитать стоимость пластиковых карт.</b>\n\n"
        "Итоговая стоимость карты зависит от:\n"
        "1) Вида пластика (он может быть белый, золотой, серебряный и золотой)\n"
        "2) От количества заказанных карт (чем больше объем, тем дешевле)\n"
        "От дополнительных функций на карте (qr-код, магнитная полоса, серийный номер и прочее)\n\n"
        "Вы всегда можете получить консультацию и посмотреть портфолио на нашем канале\n"
        "https://t.me/pink_cardrnd\n\n"
        "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/personal_items - Выбрать дополнительные материалы\n"
        "/calculate - Рассчитать общую стоимость\n\n\n"
        "Чтобы начать, выберите количество карточек:"
    )

    # Отправка полного текста отдельным сообщением
    bot.send_message(chat_id, full_text, parse_mode='HTML', reply_markup=markup_start)

    logging.info("Command /start executed")

# Обработчик текстовых сообщений для команды /start
@bot.message_handler(func=lambda message: message.text in [
    "до 100 карточек",
    "от 100 до 200 карточек",
    "от 200 до 300 карточек",
    "от 500 до 700 карточек",
    "от 700 до 1000 карточек",
    "от 1000 до 2000 карточек",
    "от 2000 до 3000 карточек",
    "от 3000 до 5000 карточек",
    "от 5000 до 10000 карточек"
])
def handle_quantity(message):
    chat_id = message.chat.id
    if chat_id not in user_state:
        user_state[chat_id] = {}
    user_state[chat_id]["quantity"] = message.text
    logging.info("user-state params has initialized (Start\ handle1)")
    bot.send_message(
        chat_id,
        "Теперь выберите тип пластика:",
        reply_markup=markup_plastic,
    )
    logging.info("handler command \ start executed")
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
    logging.info("user-state params has initialized (Start\ handle2)")
    bot.send_message(
        chat_id,
        "Хотите добавить дополнительные элементы? Выберите или нажмите 'Готово':",
        reply_markup=markup_pers,
    )
    logging.info("handle plastic command \ start executed")
    logging.info(f"User {chat_id} selected plastic: {message.text}")

#обработчик команы /chipcards
@bot.message_handler(commands=["chipcards"])
def chipcards(message):
    chat_id = message.chat.id
    if chat_id not in user_state:
        user_state[chat_id] = {}
    user_state[chat_id]["chip_type"] = None
    user_state[chat_id]["chip_quantity"] = None
    logging.info("user-state params has initialized (chipcards)")
    bot.send_message(chat_id, "Выберите тип чипа:", reply_markup=markup_chip_type)
    logging.info("Command /chipcards executed")

#обработчик выбора типа чипа
@bot.message_handler(func=lambda message: message.text in ["Em-Marine", "Mifare"])
def handle_chip_type(message):
    chat_id = message.chat.id
    if chat_id not in user_state:
        user_state[chat_id] = {}
    user_state[chat_id]["chip_type"] = message.text
    logging.info("user-state params has initialized (chipcards\ handle1)")
    bot.send_message(chat_id, "Теперь выберите количество карт с чипами:", reply_markup=markup_chip_quantity)
    logging.info("handle chip_type command \ chipcards executed")
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
    logging.info(f"User chose {message.text} and {user_state[chat_id]["chyp_type"]}")
    calculate_chip_cost(chat_id)
    logging.info("Func calculate_chip_cost executed")

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
@bot.message_handler(commands=["personal_items"])
def pers(message):
    chat_id = message.chat.id
    if chat_id not in user_state:
        user_state[chat_id] = {}
    if "extras" not in user_state[chat_id]:
        user_state[chat_id]["extras"] = []
    logging.info("user-state params has initialized (pers)")
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

    # Проверка, что выбранный диапазон находится в prices
    if state["quantity"] not in prices:
        bot.send_message(chat_id, "Выбранный диапазон количества карточек недействителен. Пожалуйста, выберите корректный диапазон.")
        return

    try:
        # Разбор диапазона количества карточек
        quantity_range = state["quantity"].split("до")
        lower_bound = int(quantity_range[0].strip().replace("от", "").strip())
        upper_bound = int(quantity_range[1].strip().replace("карточек", "").strip())

        # Базовая цена за единицу пластика
        base_price_per_unit = prices[state["quantity"]][state["plastic"]]

        # Стоимость дополнительных элементов за единицу
        extra_prices_per_unit = {}
        for extra in state["extras"]:
            extra_price = prices[state["quantity"]].get(extra, 0)
            if isinstance(extra_price, str):
                bot.send_message(chat_id, f"Элемент '{extra}' не имеет фиксированной цены.")
                continue
            extra_prices_per_unit[extra] = extra_price

        # Расчет общей стоимости для нижней и верхней границ
        def calculate_total_cost(quantity):
            total_cost = base_price_per_unit * quantity
            for extra, extra_price in extra_prices_per_unit.items():
                total_cost += extra_price * quantity
            return total_cost

        total_cost_lower = calculate_total_cost(lower_bound)
        total_cost_upper = calculate_total_cost(upper_bound)

        # Создание изображения
        try:
            # Создаем изображение карты
            image_path = create_card_image(chat_id)
            # Используем временный файл для отправки изображения
            with temporary_file(image_path) as photo_path:
                with open(photo_path, 'rb') as photo:
                    # Проверяем, добавлен ли элемент "Магнитный винил (Магниты)"
                    if "Магнитный винил (Магниты)" in state.get("extras", []):
                        bot.send_photo(
                            chat_id,
                            photo,
                            caption=(
                            f"Итоговая стоимость для {lower_bound} карточек: {total_cost_lower} Р\n"
                            f"Итоговая стоимость для {upper_bound} карточек: {total_cost_upper} Р\n"
                            f"Магнитный винил (Магниты) будет добавлен в итоговой вариант физического варианта карточки."
                            "По поводу заказа писать сюда: @Olga_rn\n"
                            "Напоминание! Это всего-лишь макет\демо реальной карточки.\n"
                            "Вы всегда можете получить консультацию и посмотреть портфолио на нашем канале\n"
                            "<a href='https://t.me/pink_cardrnd'>https://t.me/pink_cardrnd</a>\n"
                            "Спасибо.\n"
                            ),parse_mode='HTML'
                        )
                    elif "Фактурное покрытие" in state.get("extras",[]):
                        bot.send_photo(
                            chat_id,
                            photo,
                            caption=(
                            f"Итоговая стоимость для {lower_bound} карточек: {total_cost_lower} Р\n"
                            f"Итоговая стоимость для {upper_bound} карточек: {total_cost_upper} Р\n"
                            f"Фактурное покрытие будет добавлено в итоговой вариант физического варианта карточки."
                            "По поводу заказа писать сюда: @Olga_rn\n"
                            "Напоминание! Это всего-лишь макет\демо реальной карточки.\n"
                            "Вы всегда можете получить консультацию и посмотреть портфолио на нашем канале\n"
                            "<a href='https://t.me/pink_cardrnd'>https://t.me/pink_cardrnd</a>\n"
                            "Спасибо.\n"
                            ),parse_mode='HTML'
                        )
                    elif "Эмбоссирование и типирование" in state.get("extras",[]):
                        bot.send_photo(
                            chat_id,
                            photo,
                            caption=(
                            f"Итоговая стоимость для {lower_bound} карточек: {total_cost_lower} Р\n"
                            f"Итоговая стоимость для {upper_bound} карточек: {total_cost_upper} Р\n"
                            f"Эмбоссирование и типирование будет добавлено в итоговой вариант физического варианта карточки.\n"
                            "По поводу заказа писать сюда: @Olga_rn\n"
                            "Напоминание! Это всего-лишь макет\демо реальной карточки.\n"
                            "Вы всегда можете получить консультацию и посмотреть портфолио на нашем канале\n"
                            "<a href='https://t.me/pink_cardrnd'>https://t.me/pink_cardrnd</a>\n"
                            "Спасибо.\n"
                            ),parse_mode='HTML'
                        )
                    elif "Тиснение (фальгирование)" in state.get("extras",[]):
                        bot.send_photo(
                            chat_id,
                            photo,
                            caption=(
                            f"Итоговая стоимость для {lower_bound} карточек: {total_cost_lower} Р\n"
                            f"Итоговая стоимость для {upper_bound} карточек: {total_cost_upper} Р\n"
                            f"Тиснение (фальгирование) будет добавлено в итоговой вариант физического варианта карточки.\n"
                            "По поводу заказа писать сюда: @Olga_rn\n"
                            "Напоминание! Это всего-лишь макет\демо реальной карточки.\n"
                            "Вы всегда можете получить консультацию и посмотреть портфолио на нашем канале\n"
                            "<a href='https://t.me/pink_cardrnd'>https://t.me/pink_cardrnd</a>\n"
                            "Спасибо.\n"
                            ),parse_mode='HTML'
                        )
                    elif "Тиснение (фальгирование)" in state.get("extras",[]):
                        bot.send_photo(
                            chat_id,
                            photo,
                            caption=(
                            f"Итоговая стоимость для {lower_bound} карточек: {total_cost_lower} Р\n"
                            f"Итоговая стоимость для {upper_bound} карточек: {total_cost_upper} Р\n"
                            f"Тиснение (фальгирование) будет добавлено в итоговой вариант физического варианта карточки.\n"
                            "По поводу заказа писать сюда: @Olga_rn\n"
                            "Напоминание! Это всего-лишь макет\демо реальной карточки.\n"
                            "Вы всегда можете получить консультацию и посмотреть портфолио на нашем канале\n"
                            "<a href='https://t.me/pink_cardrnd'>https://t.me/pink_cardrnd</a>\n"
                            "Спасибо.\n"
                            ),parse_mode='HTML'
                        )
                    else:
                        bot.send_photo(
                            chat_id,
                            photo,
                            caption=(
                            f"Итоговая стоимость для {lower_bound} карточек: {total_cost_lower} Р\n"
                            f"Итоговая стоимость для {upper_bound} карточек: {total_cost_upper} Р\n"
                            "По поводу заказа писать сюда: @Olga_rn\n"
                            "Напоминание! Это всего-лишь макет\демо реальной карточки.\n"
                            "Вы всегда можете получить консультацию и посмотреть портфолио на нашем канале\n"
                            "<a href='https://t.me/pink_cardrnd'>https://t.me/pink_cardrnd</a>\n"
                            "Спасибо.\n"
                            ),parse_mode='HTML'
                        )

        except Exception as e:
            logging.error(f"Error creating image: {e}")
            bot.send_message(
                chat_id,
                (
                    f"Итоговая стоимость для {lower_bound} карточек: {total_cost_lower} Р\n"
                    f"Итоговая стоимость для {upper_bound} карточек: {total_cost_upper} Р\n"
                    "По поводу заказа писать сюда: @Olga_rn"
                    "Напоминание! Это всего-лишь макет\демо реальной карточки.\n"
                    "Вы всегда можете получить консультацию и посмотреть портфолио на нашем канале\n"
                    "https://t.me/pink_cardrnd\n"
                    "Спасибо.\n"
                ),parse_mode='HTML'
            )

        logging.info(f"User {chat_id} calculated total cost: Lower bound {lower_bound}, Upper bound {upper_bound}")

    except Exception as e:
        logging.error(f"Error processing quantity range: {e}")
        bot.send_message(chat_id, "Произошла ошибка при обработке диапазона количества карточек. Пожалуйста, выберите корректный диапазон.")

# Обработчик ошибок
@bot.message_handler(func=lambda message: True)
def handle_error(message):
    bot.reply_to(message, "Неизвестная команда. Пожалуйста, используйте кнопки.")
    logging.info("handle_error has executed ;(")
    logging.error(f"Unknown command received: {message.text}")

cleanup_thread=threading.Thread(target=periodic_cleanup,daemon=True)
cleanup_thread.start()

# Основная функция запуска бота
def main() -> None:
    # Удаляем вебхук
    try:
        bot.delete_webhook()
        logger.info("Webhook removed")
    except Exception as e:
        logging.error(f"Error deleting webhook: {e}")

    # Запускаем polling
    logger.info("Bot started with polling")
    cleanup_temp_file()
    bot.polling()
if __name__ == "__main__":
    main()