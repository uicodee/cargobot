from aiogram import types


def cancel(_):
    keyboard = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [types.InlineKeyboardButton(text=_('❌ Bekor qilish'), callback_data='cancel')]
    ])
    return keyboard

