from aiogram import Dispatcher, types
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.callback_datas.callback_datas import cb_language
from tgbot.keyboards.main_menu import main_menu_markup
from tgbot.models import User
from tgbot.config import _


async def user_start(m: types.Message, session: AsyncSession):
    data = await session.execute(select(User.user_id).filter(User.user_id == m.from_user.id))
    if data.scalar() is None:
        await m.answer(
            text="Assalomu Alaykum, tilni tanlang\n"
                 "Hello, choose your language\n",
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [types.InlineKeyboardButton(text="🇺🇸 English", callback_data=cb_language.new(language_code="en"))],
                    [types.InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data=cb_language.new(language_code="uz"))],
                ]
            )
        )
    else:
        await m.answer(
            text=_('Asosiy menu'),
            reply_markup=main_menu_markup()
        )


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
