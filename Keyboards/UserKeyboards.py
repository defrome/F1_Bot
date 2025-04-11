from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Config.config import F1_TEAMS
from Keyboards.Consts.InlineConsts import InlineConstructor

main_buttons = [
    {"text": "Календарь гонок", "callback_data": "race_calendar"},
    {"text": "Команды", "callback_data": "teams"},
    {"text": "Таблица", "callback_data": "standings"},
    {"text": "Последняя гонка", "callback_data": "last_race"},
]

def get_teams_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура со списком команд"""
    builder = InlineKeyboardBuilder()
    for team in F1_TEAMS.keys():
        builder.button(text=team, callback_data=f"team_{team}")
    builder.button(text="🔙 Назад", callback_data="main_menu")
    builder.adjust(2)  # 2 кнопки в ряд
    return builder.as_markup()

def get_drivers_keyboard(team: str) -> InlineKeyboardMarkup:
    """Клавиатура с гонщиками конкретной команды"""
    builder = InlineKeyboardBuilder()
    for driver in F1_TEAMS[team]:
        builder.button(text=driver, callback_data=f"driver_{driver}")
    builder.button(text="🔙 К командам", callback_data="teams_menu")
    builder.adjust(1)  # 1 кнопка в ряд
    return builder.as_markup()

def get_back_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру с кнопкой 'Назад'"""
    keyboard = [
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_main_keyboard() -> InlineKeyboardMarkup:
    return InlineConstructor.create_kb(
        buttons=main_buttons,
        schema=[1, 2, 2],
    )
