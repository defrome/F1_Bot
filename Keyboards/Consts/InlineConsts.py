from typing import Optional, Union, List, Dict

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class InlineConstructor:
    @staticmethod
    def create_kb(
            buttons: List[Dict[str, Union[str, Dict]]],
            schema: List[int],
            back_button: Optional[Dict[str, Union[str, Dict]]] = None
    ) -> InlineKeyboardMarkup:
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
