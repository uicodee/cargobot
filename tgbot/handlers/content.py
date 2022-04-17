from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from tgbot.config import _
from tgbot.keyboards.cancel import cancel

from tgbot.states.states import SenderForm, ReceiverForm, BoxInfo


async def get_surname_sender(m: types.Message, state: FSMContext):
    surname = m.text
    await state.update_data(surname_sender=surname)
    await m.answer(
        text=_('👤 Ismingizni kiriting')
    )
    await SenderForm.name.set()


async def get_name_sender(m: types.Message, state: FSMContext):
    name = m.text
    await state.update_data(name_sender=name)
    await m.answer(text=_('📍 Adresingizni kiriting'))
    await SenderForm.address.set()


async def get_address_sender(m: types.Message, state: FSMContext):
    address = m.text
    await state.update_data(address_sender=address)
    await m.answer(text=_('🌇 Shahringizni kiriting'))
    await SenderForm.city.set()


async def get_city_sender(m: types.Message, state: FSMContext):
    city = m.text
    await state.update_data(city_sender=city)
    await m.answer(
        text=_('Telefon raqamingizni tugma yordamida kiriting 👇🏻'),
        reply_markup=types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True, keyboard=[
            [types.KeyboardButton(text=_('📞 Raqamni ulashish'), request_contact=True)],
        ])
    )
    await SenderForm.phone.set()


async def get_phone_sender(m: types.Message, state: FSMContext):
    if m.content_type != "contact":
        await m.answer(
            text=_('❌ Iltimos faqat tugma yordamida kiriting')
        )
    else:
        phone = m.contact.phone_number
        await state.update_data(phone_sender=phone)
        data = await state.get_data()
        await m.answer(
            text=_('📋 Ma\'lumotlarni qayta tekshirib oling\n\n'
                   '👤 <b>Familiya:</b> {surname_sender}\n'
                   '👤 <b>Ism:</b> {name_sender}\n'
                   '📍 <b>Manzil:</b> {address_sender}\n'
                   '🌇 <b>Shahar:</b> {city_sender}\n'
                   '📞 <b>Telefon:</b> {phone_sender}\n'
                   ).format(**data),
            reply_markup=types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                [types.InlineKeyboardButton(text=_('✅ Tasdiqlash'), callback_data='confirm')],
                [types.InlineKeyboardButton(text=_('❌ Bekor qilish'), callback_data='cancel')]
            ])
        )
        await state.reset_state(with_data=False)


# Receiver state
async def get_surname_receiver(m: types.Message, state: FSMContext):
    surname = m.text
    await state.update_data(surname_receiver=surname)
    await m.answer(text=_('👤 Qabul qiluvchi ismini kiriting'))
    await ReceiverForm.name.set()


async def get_name_receiver(m: types.Message, state: FSMContext):
    name = m.text
    await state.update_data(name_receiver=name)
    await m.answer(text=_('📍 Qabul qiluvchi adresini kiriting'))
    await ReceiverForm.address.set()


async def get_address_receiver(m: types.Message, state: FSMContext):
    address = m.text
    await state.update_data(address_receiver=address)
    await m.answer(text=_('🌇 Qabul qiluvchi shahrini kiriting'))
    await ReceiverForm.city.set()


async def get_city_receiver(m: types.Message, state: FSMContext):
    city = m.text
    await state.update_data(city_receiver=city)
    await m.answer(
        text=_('📞 Qabul qiluvchi telefonini raqamini kiriting')
    )
    await ReceiverForm.phone.set()


async def get_phone_receiver(m: types.Message, state: FSMContext):
    phone = m.text
    await state.update_data(phone_receiver=phone)
    data = await state.get_data()
    await m.answer(
        text=_('📋 Ma\'lumotlarni qayta tekshirib oling\n\n'
               '👤 <b>Qabul qiluvchi familiyasi:</b> {surname_receiver}\n'
               '👤 <b>Qabul qiluvchi ismi:</b> {name_receiver}\n'
               '📍 <b>Qabul qiluvchi manzili:</b> {address_receiver}\n'
               '🌇 <b>Qabul qiluvchi shahri:</b> {city_receiver}\n'
               '📞 <b>Qabul qiluvchi telefon raqami:</b> {phone_receiver}\n'
               ).format(**data),
        reply_markup=types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [types.InlineKeyboardButton(text=_('✅ Tasdiqlash'), callback_data='confirm_receiver')],
            [types.InlineKeyboardButton(text=_('❌ Bekor qilish'), callback_data='cancel')]
        ])
    )
    await state.reset_state(with_data=False)


async def get_box_info(m: types.Message, state: FSMContext):
    box_info = m.text
    await state.update_data(box_info=box_info)
    await m.answer(
        text=_('📦 Buyrtma nimadan iborat?')
    )
    await BoxInfo.content.set()


async def get_content(m: types.Message, state: FSMContext):
    content = m.text
    await state.update_data(content=content)
    await m.answer(
        text='🗳 Buyurtmalar sonini kiriting'
    )
    await BoxInfo.count.set()


async def get_count(m: types.Message, state: FSMContext):
    count = m.text
    if not count.isdigit():
        await m.answer(
            text=_('Iltimos faqat son kiriting')
        )
    else:
        await state.update_data(count=count)
        await m.answer(
            text='💲 Buyurtma narxini kiriting'
        )
        await BoxInfo.price.set()


async def get_price(m: types.Message, state: FSMContext):
    price = m.text
    await state.update_data(price=price)
    data = await state.get_data()
    txt = _('📤 Yuboruvchi:\n\n'
            '👤 <b>Familiya:</b> {surname_sender}\n'
            '👤 <b>Ism:</b> {name_sender}\n'
            '📍 <b>Manzil:</b> {address_sender}\n'
            '🌇 <b>Shahar:</b> {city_sender}\n'
            '📞 <b>Telefon:</b> {phone_sender}\n\n'
            '📥 Qabul qiluvchi:\n\n'
            '👤 <b>Qabul qiluvchi familiyasi:</b> {surname_receiver}\n'
            '👤 <b>Qabul qiluvchi ismi:</b> {name_receiver}\n'
            '📍 <b>Qabul qiluvchi manzili:</b> {address_receiver}\n'
            '🌇 <b>Qabul qiluvchi shahri:</b> {city_receiver}\n'
            '📞 <b>Qabul qiluvchi telefon raqami:</b> {phone_receiver}\n\n'
            '📦 Buyurtma:\n\n'
            '📦 <b>Buyurtma xaqida ma\'lumot:</b> {box_info}\n'
            '🏷 <b>Buyutma tarkibi:</b> {content}\n'
            '🗳 <b>Buyurtmalar soni:</b> {count}\n'
            '💲 <b>Buyurtma narxi: </b> {price}\n'
            )
    await m.answer(
        text=txt.format(**data),
        reply_markup=types.InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [types.InlineKeyboardButton(text=_('✅ Tasdiqlash va yuborish'), callback_data='finish')],
            [types.InlineKeyboardButton(text=_('❌ Bekor qilish'), callback_data='cancel')]
        ])
    )


def register_states(dp: Dispatcher):
    dp.register_message_handler(get_surname_sender, state=SenderForm.surname)
    dp.register_message_handler(get_name_sender, state=SenderForm.name)
    dp.register_message_handler(get_address_sender, state=SenderForm.address)
    dp.register_message_handler(get_city_sender, state=SenderForm.city)
    dp.register_message_handler(get_phone_sender, state=SenderForm.phone, content_types=types.ContentTypes.CONTACT)

    dp.register_message_handler(get_surname_receiver, state=ReceiverForm.surname)
    dp.register_message_handler(get_name_receiver, state=ReceiverForm.name)
    dp.register_message_handler(get_address_receiver, state=ReceiverForm.address)
    dp.register_message_handler(get_city_receiver, state=ReceiverForm.city)
    dp.register_message_handler(get_phone_receiver, state=ReceiverForm.phone)
    dp.register_message_handler(get_box_info, state=BoxInfo.box_info)
    dp.register_message_handler(get_content, state=BoxInfo.content)
    dp.register_message_handler(get_count, state=BoxInfo.count)
    dp.register_message_handler(get_price, state=BoxInfo.price)

