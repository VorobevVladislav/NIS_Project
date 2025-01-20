from gigachat import GigaChat
from config import GIGACHATKEY
import requests


# Шаблоны для извлечения текста статьи и её суммаризации
extract_template = (
    """Получите полный текст статьи с названием "{title}" и верните его."""
)
summarize_template = """Суммируйте следующий текст: {text}"""




# Функция для получения текста статьи по ссылке и по названию
def get_article_text(url, title):
    # extract_prompt = extract_template.format(title=title)

    text = requests.get(url).text
    with GigaChat(credentials=GIGACHATKEY, verify_ssl_certs=False) as giga:
        response = giga.chat(
            f'Вот полный html-документ страницы: {text}.\nПолучите полный текст статьи с названием "{title}" и верните его. Не нужно возвращать ничего кроме этого текста, никаких объяснений.'
        )
    return response.choices[0].message.content


# Функция для суммаризации статьи
def summarize_article(text):
    # Пример единичного запроса к модели без диалога
    with GigaChat(credentials=GIGACHATKEY, verify_ssl_certs=False) as giga:
        response = giga.chat(f"Сумаризируйте следующий текст: {text}")
    return response.choices[0].message.content

# Написать статью по названию
def writeArticle(name):
    with GigaChat(credentials=GIGACHATKEY, verify_ssl_certs=False) as giga:
        response = giga.chat(f"Напишите статью на тему: {name}")
    return response.choices[0].message.content

# print("\n" * 10)
# print("gtybc")
# print(get_article_text("https://cyberleninka.ru/article/c/mathematics", "Адаптивный алгоритм разнесения соединений по слоям"))
# print("\n" * 10)
# print(
#     summarize_article(
#         """Aiogram — это высокоуровневая асинхронная библиотека для Telegram Bot API. Позволяет реализовывать ботов, которые могут работать параллельно с несколькими пользователями, не ожидая ответа от каждого из них.

# Библиотека использует синтаксис async/await, который позволяет программе выполнять несколько задач одновременно и эффективно управлять потоком выполнения.

# Aiogram предлагает множество инструментов и полный доступ к Telegram API для работы с сообщениями, клавиатурой, медиафайлами и другими функциями.

# Библиотека имеет интуитивно понятный интерфейс, который помогает сосредоточиться на логике взаимодействия бота с пользователем и минимизировать необходимость глубоко погружаться в детали реализации Telegram API.

# Aiogram имеет подробную документацию и большое русскоязычное комьюнити."""
#     )
# )
