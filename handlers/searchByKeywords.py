from classes import RegistrationState, SearchStates, FSMData, CallbackDataFilter
from functions.allFunctions import search_articles
import keyboards as kb
from functions.gigaChat import writeArticle

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from aiogram import F

searchByKeywords = Router()


# # Найти статью по ключевым словам
# # Запрос источника для поиска
# @searchByKeywords.message(
#     (F.text == "/find_by_keywords") | (F.text == "Найти статью по ключевым словам"),
#     RegistrationState.confirmated,
#     flags={"priority": 10},
# )
# async def process_source(message: Message, state: FSMContext):
#     await message.answer(
#         "Введите источник, на котором хотите производить поиск статей (название): "
#     )
#     await state.set_state(SearchStates.waiting_for_source)


# # Обработка источника для поиска и запрос ключевых слов для поиска
# @searchByKeywords.message(SearchStates.waiting_for_source)
# async def process_source(message: Message, state: FSMContext):
#     fsm_data = FSMData(source=message.text)
#     await state.update_data(source=fsm_data.source)
#     print(f"Сохранен источник: {fsm_data.source}")
#     await message.answer(
#         "Отлично! Теперь введите ключевые слова для поиска через пробел:"
#     )
#     await state.set_state(SearchStates.waiting_for_keywords)


# # Обработка ключевых слов для поиска и запуск функции поиска
# @searchByKeywords.message(SearchStates.waiting_for_keywords)
# async def process_keywords(message: Message, state: FSMContext):
#     data = await state.get_data()
#     fsm_data = FSMData(source=data["source"], keywords=message.text)
#     await state.update_data(keywords=fsm_data.keywords)
#     print(f"Сохранены ключевые слова: {fsm_data.keywords}")
#     await search_articles(message, state)
#     await state.clear()


# # Запрос названия статьи
# @router.message(
#     (F.text == "/find_by_keywords") | (F.text == "Найти статью по ключевым словам"),
#     RegistrationState.confirmated
# )
# async def process_source_url_request(message: Message, state: FSMContext):
#     await message.answer("Введите ссылку на источник, где нужно искать статью:")
#     await state.set_state(SearchStates.waiting_for_source)


# # Обработка ссылки на источник и запрос названия статьи
# @router.message(SearchStates.waiting_for_source)
# async def process_source_url(message: Message, state: FSMContext):
#     source_url = message.text
#     await state.update_data(source_url=source_url)
#     await message.answer("Отлично! Теперь введите название статьи для поиска:")
#     await state.set_state(SearchStates.waiting_for_title)


# # Обработка названия статьи и выполнение поиска
# @router.message(SearchStates.waiting_for_title)
# async def process_title(message: Message, state: FSMContext):
#     title = message.text
#     data = await state.get_data()
#     source_url = data.get("source_url")

#     # Вызов функции поиска по названию на источнике
#     await search_by_title(message, source_url, title)
#     await state.clear()


# Запрос источника для поиска
@searchByKeywords.message(
    (F.text == "/find_by_keywords") | (F.text == "Найти статью по ключевым словам"),
    RegistrationState.confirmated,
    flags={"priority": 10},
)
async def process_source(message: Message, state: FSMContext):
    await message.answer("Введите тему для поиска статьи:")
    await state.set_state(SearchStates.waiting_for_keywords)


# Обработка ключевых слов для поиска и запуск функции поиска
@searchByKeywords.message(SearchStates.waiting_for_keywords)
async def process_keywords(message: Message, state: FSMContext):
    kb.clearArticlesNames()  # подготовка массивов для новых элементов
    fsm_data = FSMData(keywords=message.text)
    await state.update_data(keywords=fsm_data.keywords)
    print(f"Сохранена тема: {fsm_data.keywords}")
    await search_articles(message, state)
    await state.set_state(RegistrationState.confirmated)
    await state.set_state(SearchStates.waiting_for_article_name)


# Инлайн кнопки с названиями статей, при нажатии выдается статья по теме
@searchByKeywords.callback_query(CallbackDataFilter(kb.articlesNames))
async def showArticle(callback: CallbackQuery):
    articleName = callback.data
    article = writeArticle(articleName)  # Предположим, что writeArticle — это функция, которая возвращает текст статьи
    await callback.message.answer(article)  # Отправляем текст статьи