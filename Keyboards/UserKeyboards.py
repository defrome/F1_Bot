from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Keyboards.Consts.InlineConsts import InlineConstructor

main_buttons = [
    {"text": "Календарь гонок", "callback_data": "race_calendar"},
    {"text": "Гонщики", "callback_data": "drivers"},
    {"text": "Команды", "callback_data": "teams"},
    {"text": "Таблица", "callback_data": "standings"},
    {"text": "Последняя гонка", "callback_data": "last_race"},
]

def get_back_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру с кнопкой 'Назад'"""
    keyboard = [
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_main_keyboard() -> InlineKeyboardMarkup:
    return InlineConstructor.create_kb(
        buttons=main_buttons,  # Используем main_buttons вместо buttons
        schema=[1, 2, 2],
    )
