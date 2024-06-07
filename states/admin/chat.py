from aiogram.dispatcher.filters.state import StatesGroup, State


class ChatState(StatesGroup):
    is_chatting = State()
