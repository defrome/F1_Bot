from typing import Optional, Union, List, Dict

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class InlineConstructor:
    @staticmethod
    def create_kb(
            buttons: List[Dict[str, Union[str, Dict]]],
            schema: List[int],
            back_button: Optional[Dict[str, Union[str, Dict]]] = None
    ) -> InlineKeyboardMarkup:
        """
        Создает InlineKeyboardMarkup из переданных кнопок и схемы.

        :param buttons: Список словарей с параметрами кнопок.
            Пример: [{"text": "Текст кнопки", "callback_data": "callback"}]
        :param schema: Схема распределения кнопок по рядам.
            Пример: [2, 1] - два ряда: в первом 2 кнопки, во втором 1.
        :param back_button: Параметры кнопки "Назад" (добавляется в конец).
            Пример: {"text": "Назад", "callback_data": "back"}
        :return: Объект InlineKeyboardMarkup
        """
        keyboard = []

        # Добавляем основные кнопки согласно схеме
        start_idx = 0
        for count in schema:
            row_buttons = buttons[start_idx:start_idx + count]
            row = []
            for button in row_buttons:
                row.append(InlineKeyboardButton(**button))
            keyboard.append(row)
            start_idx += count

        remaining_buttons = buttons[start_idx:]
        if remaining_buttons:
            for button in remaining_buttons:
                keyboard.append([InlineKeyboardButton(**button)])
        if back_button:
            keyboard.append([InlineKeyboardButton(**back_button)])

        return InlineKeyboardMarkup(inline_keyboard=keyboard)
