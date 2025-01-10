# spacy-trees-tgbot-rus

### **Описание проекта**

Этот проект представляет собой Telegram-бота для визуализации синтаксических зависимостей слов в предложениях на русском языке. Бот использует библиотеку spaCy для анализа текста и создания визуализации зависимостей в формате изображений. Каждое предложение, отправленное пользователем, обрабатывается отдельно, и для него генерируется PNG-картинка, показывающая связи между словами.

### **Основные функции** 

1. Обработка текста на русском языке: анализ текста с использованием библиотеки spaCy, разделение текста на предложения, опрделение синтаксических зависимостей и частей речи. 
2. Создание визуализаций: генерация SVG-файлов с зависимостями между словами, конвертация SVG в PNG с использованием утилиты rsvg-convert.
3. Инициализация Telegram-бота и настройка интерфейса: встроенные кнопки для получения дополнительной информации о боте или начала работы с текстом,


### **Установка**

**1. Клонирование репозитория**

Склонируйте проект с GitHub:

`git clone <URL репозитория> cd <папка проекта>`

**2. Создание виртуального окружения**

Создайте виртуальное окружение и активируйте его:

`python3.11 -m venv venv`

`source venv/bin/activate`# Для Linux/MacOS

`venv\Scripts\activate`     # Для Windows

**3. Установка зависимостей**

Установите зависимости из файла requirements.txt:

`pip install -r requirements.txt`

**4. Настройка файла .env**

Создайте файл .env в корне проекта и добавьте в него токен вашего Telegram-бота:

`TOKEN=ваш_токен_бота`

Если у вас еще нет токена, создайте бота через BotFather в Telegram и получите токен.

**5. Запуск проекта**

Запустите бота:

`python main.py`

После запуска бот будет ожидать сообщения в Telegram.

### **Как использовать**
1.	В Telegram найдите своего бота и начните с команды /start. 
2. Выберите действие:
- Подробнее: получить описание возможностей бота.
- Генерация: отправьте текст на русском языке для анализа.
3.	Отправьте текст, и бот создаст изображения с зависимостями для каждого предложения.

### **Логирование**

Все ошибки и события записываются в файл log.log, который создается в корневой папке проекта. Если бот не работает или произошла ошибка, проверьте этот файл для диагностики.

### **Зависимости**

Бот использует следующие библиотеки и утилиты:
- **Python 3.12**: Рекомендуемая версия Python.
- **spaCy**: Анализ текста и синтаксических зависимостей.
- **telebot**: Взаимодействие с Telegram API.
- **dotenv**: Для работы с переменными окружения.
- **rsvg-convert**: Для конвертации SVG в PNG (должна быть установлена глобально).

### Установка resvg-convert на MacOS:

`brew install librsvg`  #  (через Homebrew)

### Установка `rsvg-convert` на Windows

1. Установите GTK:
   - Скачайте [GTK для Windows](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases).
   - Установите GTK, выбрав последнюю версию. Запомните путь установки (например, `C:\Program Files\GTK3-Runtime`).

2. Добавьте путь к `rsvg-convert.exe` в системную переменную PATH:
   - Перейдите в `C:\Program Files\GTK3-Runtime\bin`.
   - Скопируйте путь и добавьте его в переменную PATH.

3. Проверьте установку:
   - Откройте командную строку и выполните:
     `rsvg-convert --version
     `

### **Описание кода**

**Основные файлы**
- **main.py**: основной файл с кодом бота.
- **requirements.txt**: список зависимостей.
- **.env**: файл для хранения токена (необходимо создать вручную через терминал или в IDE PyCharm: _File -> New..._).

**Ключевые функции**
1. **svg_to_png(svg_content)**: конвертирует SVG в PNG.
2. **send_welcome(message)**: отправляет приветственное сообщение с кнопками.
3. **spacy_svg(message)**: обрабатывает текст и создает визуализацию зависимостей.
4. **callback_query(call)**: обрабатывает нажатия на встроенные кнопки.

### **Примечания**
Если файл .env отсутствует или токен не указан, программа завершится с сообщением об ошибке, а подробности будут записаны в лог.

