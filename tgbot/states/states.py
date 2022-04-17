from aiogram.dispatcher.filters.state import StatesGroup, State


class SenderForm(StatesGroup):
    surname = State()
    name = State()
    address = State()
    city = State()
    phone = State()


class ReceiverForm(StatesGroup):
    surname = State()
    name = State()
    address = State()
    city = State()
    phone = State()


class BoxInfo(StatesGroup):
    box_info = State()
    content = State()
    count = State()
    price = State()