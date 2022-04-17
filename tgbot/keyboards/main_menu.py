from aiogram import types
from tgbot.config import _


def main_menu_markup(**kwargs):
    print(kwargs)
    main_menu = types.InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [types.InlineKeyboardButton(text=_("🧾 Ro'yxatdan o'tish", locale=kwargs.get('locale')), callback_data='start_reg')],
            [types.InlineKeyboardButton(text=_("🌐 Tilni o'zgartirish", locale=kwargs.get('locale')), callback_data='set_language')],
        ]
    )
    return main_menu