import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
from dotenv import load_dotenv

from Config.config import F1_TEAMS, F1_2025_CALENDAR, F1_TABLE_2025
from Keyboards.UserKeyboards import UserKeyboards, UserKeyboards

from Parse_web.calen_parse import Parser

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

logging.basicConfig(level=logging.INFO)

keyboard_builder = UserKeyboards()

# Загрузка переменных окружения
load_dotenv()

# Инициализация бота
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Токен бота не найден! Убедитесь, что он задан в файле .env")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хендлеры команд
@dp.message(Command("start"))
async def start_command(message: Message) -> None:
    await message.answer(
        "🏎 Добро пожаловать в бота Formula 1!\n"
        "Выберите интересующий вас раздел:",
        reply_markup = keyboard_builder.get_main_keyboard()
    )

@dp.message(Command("menu"))
async def menu_command(message: Message) -> None:
    await message.answer(
        "🏎 Главное меню:",
        reply_markup = keyboard_builder.get_main_keyboard()
    )

# Основные callback-обработчики
@dp.callback_query(lambda c: c.data == "main_menu")
async def main_menu_callback(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🏎 Главное меню:",
        reply_markup = keyboard_builder.get_main_keyboard()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "teams")
async def teams_callback(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🏁 Выберите команду:",
        reply_markup = keyboard_builder.get_teams_keyboard()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "teams_menu")
async def back_to_teams_callback(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🏁 Выберите команду:",
        reply_markup = keyboard_builder.get_teams_keyboard()
    )
    await callback.answer()

# Обработчики для команд и гонщиков
@dp.callback_query(lambda c: c.data.startswith("team_"))
async def team_selected_callback(callback: types.CallbackQuery):
    team = callback.data.split("_")[1]
    await callback.message.edit_text(
        f"🏎 Состав команды {team}:",
        reply_markup = keyboard_builder.get_drivers_keyboard(team)
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("driver_"))
async def driver_selected_callback(callback: types.CallbackQuery):
    driver = callback.data.split("_")[1]
    # Здесь можно добавить API-запрос для получения информации о гонщике
    await callback.message.edit_text(
        f"👤 Гонщик: {driver}\n\n"
        f"Команда: {next(team for team, drivers in F1_TEAMS.items() if driver in drivers)}\n"
        "Дополнительная информация будет здесь...",
        reply_markup = keyboard_builder.get_back_keyboard()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("race_"))
async def race_selected_callback(callback: types.CallbackQuery):
    race = callback.data.split("_")[1]

    race_info = Parser.get_calendar()[race]

    message_text = f'{race}\n'

    for part in race_info:
        message_text += f'{part[0].lstrip(f'{race} ')} {part[1]} {part[2]}\n'

    await callback.message.edit_text(
        message_text,
        reply_markup = keyboard_builder.get_back_keyboard()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "race_calendar")
async def race_calendar_callback(callback: types.CallbackQuery):
    try:
        # calendar_text = "🗓 Календарь гонок 2025:\n\n"


        # sorted_races = sorted(F1_2025_CALENDAR.items(), key=lambda x: x[0])

        # for race_num, race_data in sorted_races:
        #     calendar_text += (
        #         f"🏁 <b>Этап {race_num}: {race_data['name']}</b>\n"
        #         f"📍 {race_data['circuit']}\n"
        #         f"📅 {race_data['date']}\n\n"
        #     )

        await callback.message.edit_text(
            "🗓 Календарь гонок 2025:",
            reply_markup = keyboard_builder.get_calendar_keyboard()
        )

        await callback.answer()
    

        # await callback.message.edit_text(
        #     calendar_text,
        #     parse_mode="HTML",
        #     reply_markup = keyboard_builder.get_back_keyboard()
        # )

    except Exception as e:
        print(f"Ошибка при отображении календаря: {e}")
        await callback.message.edit_text(
            "❌ Произошла ошибка при загрузке календаря гонок",
            reply_markup = keyboard_builder.get_back_keyboard()
        )
    finally:
        await callback.answer()


@dp.callback_query(lambda c: c.data == "standings")
async def standings_callback(callback: types.CallbackQuery):
    try:
        standings_text = (
            "🏆 <b>Турнирная таблица 2025</b>\n"
            "══════════════════════\n"
            "<b>Место | Пилот | Очки | Победы | Подиумы</b>\n"
            "══════════════════════\n"
        )

        for position, driver in F1_TABLE_2025.items():
            flag = f"🏴" if driver["country"] == "Великобритания" else f"🇳🇱" if driver[
                                                                                   "country"] == "Нидерланды" else f"🇦🇺" if \
            driver["country"] == "Австралия" else f"🇮🇹" if driver["country"] == "Италия" else f"🇲🇨" if driver[
                                                                                                           "country"] == "Монако" else f"🇹🇭" if \
            driver["country"] == "Таиланд" else f"🇨🇦" if driver["country"] == "Канада" else f"🇩🇪" if driver[
                                                                                                         "country"] == "Германия" else f"🇯🇵" if \
            driver["country"] == "Япония" else f"🇪🇸" if driver["country"] == "Испания" else f"🇳🇿" if driver[
                                                                                                         "country"] == "Новая Зеландия" else f"🇧🇷" if \
            driver["country"] == "Бразилия" else f"🇫🇷"

            standings_text += (
                f"{position:2d} | {flag} {driver['name']} | "
                f"{driver['points']:3d} | {driver['wins']:2d} | "
                f"{driver['podiums']:2d}\n"
                f"      {driver['team']}\n"
                "────────────────────\n"
            )

        await callback.message.edit_text(
            standings_text,
            parse_mode="HTML",
            reply_markup = keyboard_builder.get_back_keyboard()
        )
    except Exception as e:
        print(f"Ошибка при отображении таблицы: {e}")
        await callback.message.edit_text(
            "❌ Произошла ошибка при загрузке турнирной таблицы",
            reply_markup = keyboard_builder.get_back_keyboard()
        )
    finally:
        await callback.answer()

@dp.callback_query(lambda c: c.data == "last_race")
async def last_race_callback(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🚩 Последняя гонка:",
        reply_markup = keyboard_builder.get_back_keyboard()
    )
    await callback.answer()


# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
