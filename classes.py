from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Filter
from aiogram.types import CallbackQuery


# Состояния для регистрации
class RegistrationState(StatesGroup):
    waiting_for_confirmation = State()
    confirmated = State()


# Класс для хранения данных
class FSMData:
    def __init__(self, source="", keywords=""):
        self.source = source
        self.keywords = keywords


# Состояния для поиска
class SearchStates(StatesGroup):
    waiting_for_source = State()  # Для поиска по ключевым словам
    waiting_for_keywords = State()  # Для поиска по ключевым словам
    waiting_for_title = State()  # Для поиска по названию
    waiting_for_article_name = State() # Ждет колбэк, чтобы взять из него название статьи


# Кастомный фильтр для проверки callback.data
class CallbackDataFilter(Filter):
    def __init__(self, articles_names):
        self.articles_names = articles_names

    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data in self.articles_names