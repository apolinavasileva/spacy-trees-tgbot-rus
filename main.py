import io  # для сохранения конвертированного изображения в буфере
import logging  # логирование ошибок в отдельный файл
import subprocess  # для работы с утилитой rsvg-convert, которая не работает напрямую с python
import sys  # для аварийного выхода из программы

import spacy  # NLP библиотека
import telebot  # для работы с telegram API
from spacy import displacy  # визуализация синтаксических зависимостей
from dotenv import load_dotenv, dotenv_values  # для чтения файла .env, в котором прописан токен бота
from telebot import types  # для создания встроенных кнопок в чат-боте

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w")  # создание файла для логирования ошибок

load_dotenv()
config = dotenv_values('.env')  # загрузка переменных из файла .env, в котором прописан токен бота
token = config.get('TOKEN')  # получение токена из файла .env
if not token:
    logging.error("Токен Telegram-бота отсутствует. Проверьте файл .env.")  # логирование ошибки
    sys.exit("Ошибка: токен Telegram-бота отсутствует. Проверьте файл .env.")  # аварийное закрытие программы, если
    # токен отсутствует

bot = telebot.TeleBot(token, parse_mode=None)  # инициализация бота с прописанным токеном

nlp = spacy.load('ru_core_news_sm')  # загрузка русскоязычной модели NLP


def svg_to_png(svg_content: str):
    """
      Конвертация svg-файла в png с использованием утилиты rsvg-convert

      Args:
          svg_content (str): svg-файл

      Returns:
          io.BytesIO: png-изображение, сохраненное в буфере.
      """
    try:
        process = subprocess.Popen(
            ["rsvg-convert", "-f", "png"],  # команда и параметры
            stdin=subprocess.PIPE,  # передача данных через стандартный ввод
            stdout=subprocess.PIPE,  # получение данных через стандартный вывод
            stderr=subprocess.PIPE  # сбор ошибок через стандартный поток ошибок
            )  # использование утилиты rsvg-convert из библиотеки librsvg с помощью subprocess, т.к. библиотека
        # изначально не предназначена для python и напрямую использована быть не может

        png_data, error = process.communicate(
            input=svg_content.encode("utf-8"))  # получение изображения png и информации
        # об ошибках

        if process.returncode != 0:
            raise RuntimeError(f"Ошибка rsvg-convert: {error.decode('utf-8')}")  # ошибка конвертации

        buffer = io.BytesIO(png_data)  # сохранение изображения в буфере (чтобы не записывать файл на компьютере)
        buffer.seek(0)  # прочтение файла с первого символа
        return buffer  # возвращает данные в буфере

    except Exception as e:
        logging.error(f"Ошибка в svg_to_png: {str(e)}")  # логирование ошибки
        raise


@bot.message_handler(commands=['start'])  # для работы с сообщением после отправки пользователем команды /start
def send_welcome(message):
    """
    Настройка приветственного сообщения, отправляемого в ответ на команду /start, с использованием встроенных кнопок.
    """
    keyboard = types.InlineKeyboardMarkup()  # загрузка клавиатуры встроенных кнопок
    button1 = types.InlineKeyboardButton("Подробнее", callback_data="button1")  # создание кнопки "подробнее"
    button2 = types.InlineKeyboardButton("Генерация", callback_data="button2")  # создание кнопки "генерация"
    keyboard.add(button1, button2)  # сохранение созданных кнопок в клавиатуре

    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! \nЭтот бот позволяет визуализировать "
                                      "синтаксические зависимости слов в"
                                      " предложениях на русском языке "
                                      "с помощью библиотеки spaCy. Выберите действие:", reply_markup=keyboard)  #
    # отправка приветственного сообщения


@bot.message_handler(func=lambda message: True, content_types=['text'])  # для обработки сообщений от пользователей
def spacy_svg(message):
    """
    Для обработки сообщений от пользователей: проверяет, соотвествует ли оно условиям, и отправляет в ответ
    png-изображения синтаксических зависимостей в предложениях.
    """
    try:
        if any(c.isalpha() and 'a' <= c <= 'z' for c in message.text.lower()):  # исключение латиницы
            bot.reply_to(message, "К сожалению, я обрабатываю текст только на русском языке 😢")
            return  # выполнение функции завершается

        if len(message.text.strip()) <= 1:  # исключение слишком коротких предложений
            bot.reply_to(message, "Предложение слишком короткое 😢")
            return  # выполнение функции завершается

        max_words = 20  # максимальное количество слов в предложении (слишком длинные предложения вызывают ошибку при
        # формировании картинки)

        doc = nlp(message.text)  # обработка текста с помощью spacy
        sentence_spans = doc.sents  # деление на предложения

        for sentence in sentence_spans:  # обработка предложений из сообщения от пользователя
            sentence_text = sentence.text.strip()  # получение отдельных слов из предложения
            if len(sentence_text.split()) > max_words:  # проверка длины предложения
                bot.reply_to(message, "Предложение слишком длинное 😢")  # слишком длинные предложения не принимаются,
                # иначе возникает ошибка преобразования из svg в png
                continue  # итерация прекращается

            svg = displacy.render(sentence, style="dep", jupyter=False)  # создание svg с синтаксическими зависимостями
            png_buffer = svg_to_png(svg)  # конвертация svg в png и сохранение в буфере

            bot.send_photo(
                message.chat.id,
                photo=png_buffer,
                caption=f"Визуализация предложения: {sentence.text}"
            )  # бот отправляет результат с подписью

            png_buffer.close()  # закрытие буфера для экономии памяти

    except telebot.apihelper.ApiException as e:
        logging.error(f"Ошибка в spacy_svg: {str(e)}")  # ошибка при обработке сообщения
        bot.reply_to(message, "Произошла ошибка при обработке текста 😢 Пожалуйста, попробуйте снова!")  # ответ пользователю


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """
    Настройка встроенных кнопок.
    """
    if call.data == "button2":  # кнопка "Генерация"
        bot.answer_callback_query(call.id)  # подтверждение нажатия кнопки и обработки запроса
        bot.send_message(call.message.chat.id, "Напишите текст на русском языке для визуализации.")  # ответ пользователю

    elif call.data == "button1":  # кнопка "Подробнее"
        info_text = (
            "Этот бот предназначен для визуализации синтаксических зависимостей предложений на русском языке. "
            "Он использует библиотеку spaCy, чтобы анализировать текст, разделять его на предложения, "
            "определять части речи, грамматические роли и синтаксическую структуру.\n\n"
            "Библиотека spaCy — это мощный инструмент для обработки естественного языка (NLP). "
            "Она позволяет разбивать текст на предложения, определять подлежащие, сказуемые, дополнения и другие связи."
            " Визуализация зависимостей помогает понять, как слова связаны между собой.\n\n"
            "Как пользоваться ботом:\n"
            "1. Напишите текст на русском языке.\n"
            "2. Бот разделит текст на предложения и обработает каждое из них.\n"
            "3. Для каждого предложения бот создаст картинку с синтаксическими зависимостями.\n\n"
            "Эта функция полезна для анализа текста, изучения грамматики, создания приложений на основе текста и "
            "многого другого."
            " Попробуйте отправить текст, чтобы увидеть, как это работает!"
        )
        bot.answer_callback_query(call.id)  # подтверждение нажатия кнопки и обработки запроса
        bot.send_message(call.message.chat.id, info_text)  # отправка сообщения пользователю


print("Бот запущен и готов к работе.")
bot.infinity_polling()  # запуск бота
