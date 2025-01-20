from initialisation import bot, llm
import keyboards as kb


import aiosqlite
from aiogram.types import Message, BotCommand, BotCommandScopeDefault
from aiogram.fsm.context import FSMContext
import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import CharacterTextSplitter
from langchain import PromptTemplate
from googlesearch import search
import re


def clean_text(text):
    # Удаляем лишние пробелы и переносы строк
    text = re.sub(r"\s+", " ", text)

    # Удаляем оставшиеся многократные пробелы после удаления шаблонов
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_main_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # Удаляем все скрипты и стили
    for script_or_style in soup(["script", "style", "noscript"]):
        script_or_style.decompose()

    # Пытаемся найти тег <article>, если он есть
    article = soup.find("article")
    if article:
        text = article.get_text(separator="\n")
    else:
        # Если <article> нет, выбираем наиболее содержательный <div>
        divs = soup.find_all("div")
        max_text = ""
        max_length = 0
        for div in divs:
            div_text = div.get_text(separator="\n").strip()
            div_length = len(div_text)
            if div_length > max_length:
                max_length = div_length
                max_text = div_text
        text = max_text

    # text = text.split('.')
    # Дополнительная очистка текста
    clean_main_text = clean_text(text)

    return clean_main_text


async def internet_search(query, k, source):
    # Выполнение поискового запроса
    links = search(query, lang="ru", num=k)
    result_array = []

    for idx, link in enumerate(links):
        try:
            if (
                (source.lower() in link.lower())
                and ("vk" not in link.lower())
                and ("facebook" not in link.lower())
            ):
                print(f"Обрабатывается ссылка {idx+1}/{k}: {link}")
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/58.0.3029.110 Safari/537.3"
                }
                response = requests.get(link, headers=headers, timeout=10)
                response.raise_for_status()
                html_content = response.text

                # Извлечение основного текста
                clean_main_text = extract_main_content(html_content)

                if not clean_main_text:
                    print(f"На странице {link} не найден основной текст.")
                    continue

                # Разбиение текста на чанки
                text_splitter = CharacterTextSplitter(
                    separator="\n", chunk_size=1000, chunk_overlap=100
                )
                chunks = text_splitter.split_text(clean_main_text)

                # Берем только первые 2 чанка
                first_two_chunks = chunks[:2]

                result_array.append(first_two_chunks)

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при загрузке {link}: {e}")
        except Exception as e:
            print(f"Ошибка при обработке контента с {link}: {e}")

    return result_array


PROMPT_TEMPLATE = """Найдите 10 статей на сайте cyberleninka,
в названиях которых встречаются ключевые слова: {keywords}.
Возвращайте только названия статей, разделяя их новой строкой."""


def find_articles(keywords):
    # Формирование запроса
    prompt = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["keywords"])
    chat_chain = prompt | llm
    result = chat_chain.invoke({"keywords": keywords})

    # Возвращаем первые 10 статей
    articles = str(result).strip().split("\n")[:10]
    return articles


# Функция для поиска статей
async def search_articles(message: Message, state: FSMContext):
    data = await state.get_data()
    keywords = data["keywords"]

    if not keywords:
        await message.answer("Произошла ошибка. Повторите ввод данных.")

    articles = find_articles(keywords)

    articles = str(articles)
    res = articles.split("\\n")[2:12]
    answer = ""
    for article in res:
        # # Находим позиции открывающей и закрывающей кавычек
        # start = article.find("**") + 1  # Позиция после открывающей кавычки
        # end = article.find("**", start)  # Позиция закрывающей кавычки
        # extracted_text = article[start : end]  # Извлекаем текст между кавычками
        # answer += extracted_text + "\n"
        answer += str(article) + "\n"

    kb.inlineArticles(articles) # в функцию должен поступить список названий статей

    if not articles:
        await message.answer("К сожалению, не удалось найти статьи по вашему запросу.")
        return
    await message.answer("Найденные статьи:")
    await message.answer(answer, reply_markup=kb.articlesButtons)


async def send_reminders():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT user_id FROM users WHERE subscribed = TRUE"
        ) as cursor:
            rows = await cursor.fetchall()

    for row in rows:
        user_id = row[0]
        await bot.send_message(
            user_id,
            "Напоминание: давно не искали статей? Зайдите в бот и попробуйте найти что-то интересное!",
        )


# Команда для старта бота
async def start_bot():
    commands = kb.globalKeyboard
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


# Подключение к базе данных
async def start_db():
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            """ CREATE TABLE IF NOT EXISTS users ( user_id INTEGER PRIMARY KEY, username TEXT, subscribed BOOLEAN DEFAULT TRUE ); """
        )
        await db.execute(
            """ CREATE TABLE IF NOT EXISTS user_requests ( id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, request TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP ); """
        )
        await db.commit()


async def checkRegistration(user_id):
    # Проверяем наличие пользователя в базе данных
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT * FROM users WHERE user_id=?", (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
    return result is not None


async def search_by_title(message: Message, source_url: str, title: str):
    try:
        # Отправляем GET-запрос на источник
        response = requests.get(source_url)
        response.raise_for_status()  # Проверяем, что запрос успешен

        # Парсим HTML-страницу
        soup = BeautifulSoup(response.text, "html.parser")

        # Ищем статьи по названию (пример для сайта с тегами <article>)
        articles = soup.find_all("article")  # Ищем все статьи
        found_articles = []

        for article in articles:
            article_title = (
                article.find("h2").text.strip() if article.find("h2") else None
            )
            if article_title and title.lower() in article_title.lower():
                article_url = (
                    article.find("a")["href"] if article.find("a") else source_url
                )
                found_articles.append({"title": article_title, "url": article_url})

        # Отправляем результаты пользователю
        if found_articles:
            for article in found_articles:
                await message.answer(
                    f"Найдена статья: {article['title']}\nСсылка: {article['url']}"
                )
        else:
            await message.answer("Статьи с таким названием не найдены.")

    except Exception as e:
        await message.answer(f"Произошла ошибка при поиске: {e}")
