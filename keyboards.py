from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import BotCommand


registration = InlineKeyboardBuilder()
registration.add(InlineKeyboardButton(text="Да", callback_data="yes"))
registration.add(InlineKeyboardButton(text="Нет", callback_data="no"))
registration = registration.adjust(2).as_markup()  # 2 кнопки в ряду

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Найти статью по ключевым словам")],
        [KeyboardButton(text="Найти статью по названию")],
        # [KeyboardButton(text="Рекомендации")],
        [
            # KeyboardButton(text="История"),
            KeyboardButton(text="Напоминания")
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню.",
)

setNotifications = InlineKeyboardBuilder()
setNotifications.add(InlineKeyboardButton(text="Включить", callback_data="able"))
setNotifications.add(InlineKeyboardButton(text="Выключить", callback_data="disable"))
setNotifications = setNotifications.adjust(2).as_markup()  # 2 кнопки в ряду

# В итог
articlesButtons = InlineKeyboardBuilder()
articlesNames = []


def clearArticlesNames():
    global articlesButtons, articlesNames  # Указываем, что работаем с глобальными переменными
    articlesButtons = InlineKeyboardBuilder()
    articlesNames = []


def inlineArticles(articles: list):
    for article in articles:
        articlesNames.append(article)
        articlesButtons.add(InlineKeyboardButton(text=article, callback_data=article))


# # Тест
# articlesButtons = InlineKeyboardBuilder()
# articlesNames = [
#     "1. **Рекомендации по разработке образовательной программы**  \n    ",
#     '2. **Методические рекомендации по изучению темы "Функции"**  \n    ',
#     "3. **Рекомендации по лечению и профилактике остеопороза у женщин в постменопаузе**  \n    ",
#     "4. **Рекомендации по применению антибактериальных препаратов в педиатрической практике**  \n    ",
#     "5. **Организация работы предприятия: рекомендации для малого бизнеса**  \n    ",
#     "6. **Рекомендации по созданию эффективной системы мотивации персонала**  \n    ",
#     "7. **Современные рекомендации по терапии болезни Крона**  \n    ",
#     "8. **Рекомендации по повышению безопасности движения на железнодорожном транспорте**  \n    ",
#     "9. **Рекомендации по проектированию и эксплуатации систем водоснабжения и канализации**  \n    ",
#     "10. **Этические рекомендации по использованию гендерно-нейтрального языка в академических публикациях**",
# ]
# for article in articlesNames:
#     articlesButtons.add(InlineKeyboardButton(text=article, callback_data=article))


globalKeyboard = [
    BotCommand(command="start", description="Старт"),
    BotCommand(
        command="find_by_keywords", description="Найти статью по ключевым словам"
    ),
    BotCommand(command="find_by_name", description="Найти статью по названию"),
    # BotCommand(command="request_history", description="История запросов"),
    # BotCommand(command="recomendations", description="Рекомендации"),
    BotCommand(command="notifications_on", description="Подключить рассылку"),
    BotCommand(command="notifications_off", description="Отключить рассылку"),
]
