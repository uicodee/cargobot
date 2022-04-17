import httplib2
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.callback_datas.callback_datas import cb_language
from tgbot.config import _
from tgbot.keyboards.main_menu import main_menu_markup
from tgbot.models.user import User
from tgbot.states.states import SenderForm, ReceiverForm, BoxInfo
from tgbot.keyboards.cancel import cancel


async def language_handler(query: types.CallbackQuery, callback_data: dict, session: AsyncSession):
    data = await session.execute(select(User.user_id).filter(User.user_id == query.from_user.id))
    if data.scalar() is None:
        await session.execute(insert(User).values(
            user_id=query.from_user.id,
            language=callback_data.get('language_code')
        ).returning('*'))
        await session.commit()
    else:
        data = {'language': callback_data.get('language_code')}
        await session.execute(update(User).where(User.user_id == query.from_user.id).values(**data))
        await session.commit()
    await query.message.edit_text(
        text=_('Asosiy menu', locale=callback_data.get('language_code')),
        reply_markup=main_menu_markup(locale=callback_data.get('language_code'))
    )


async def start_registration(query: types.CallbackQuery):
    await query.message.edit_text(
        text=_('👤 Familiyangizni kiriting')
    )
    await SenderForm.surname.set()


async def confirm_handler(query: types.CallbackQuery):
    await query.message.edit_text(
        text=_('👤 Qabul qiluvchi familiyasini kiriting')
    )
    await ReceiverForm.surname.set()


async def confirm_receiver(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text(
        text=_('Yubormoqchi bo\'lgan buyurtamngiz xaqida ma\'lumot bering')
    )
    await BoxInfo.box_info.set()


def get_service_sacc():
    creds_json = "tgbot/config-google.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)


async def add_to_gsheet(data):
    service = get_service_sacc()
    sheet = service.spreadsheets()

    sheet_id = "1-aFkESgFsNeTKjfzUu0WAuGmC5D42B_Ub_SdhG7FdcA"
    a = [
        [
            data['surname_sender'],
            data['name_sender'],
            data['address_sender'],
            data['city_sender'],
            data['phone_sender'],
        ]
    ]
    b = [
        [
            data['surname_receiver'],
            data['name_receiver'],
            data['address_receiver'],
            data['city_receiver'],
            data['phone_receiver'],

        ]
    ]
    c = [
        [
            data['box_info'],
            data['content'],
            data['count'],
            data['price'],
        ]
    ]
    sheet.values().append(
        spreadsheetId=sheet_id,
        range="Лист1!B2",
        valueInputOption="RAW",
        body={'values': a}
    ).execute()
    sheet.values().append(
        spreadsheetId=sheet_id,
        range="Лист1!G2",
        valueInputOption="RAW",
        body={'values': b}
    ).execute()
    sheet.values().append(
        spreadsheetId=sheet_id,
        range="Лист1!L2",
        valueInputOption="RAW",
        body={'values': c}
    ).execute()


async def save_data(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await add_to_gsheet(data=data)
    await query.message.edit_text(
        text=_('Buyurtmangiz qo\'shildi!')
    )


async def cancel_handler(query: types.CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=True)
    await query.message.edit_text(_('❌ Bekor qilindi'))


async def change_language(query: types.CallbackQuery):
    await query.message.edit_text(
        text="Assalomu Alaykum, tilni tanlang\n"
             "Hello, choose your language\n",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="🇺🇸 English", callback_data=cb_language.new(language_code="en"))],
                [types.InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data=cb_language.new(language_code="uz"))],
            ]
        )
    )


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(language_handler, cb_language.filter())
    dp.register_callback_query_handler(start_registration, text='start_reg')
    dp.register_callback_query_handler(confirm_handler, text='confirm')
    dp.register_callback_query_handler(confirm_receiver, text='confirm_receiver')
    dp.register_callback_query_handler(save_data, text='finish', state="*")
    dp.register_callback_query_handler(cancel_handler, text='cancel', state="*")
    dp.register_callback_query_handler(change_language, text='set_language')
