import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import CantParseEntities
from aiogram_calendar import dialog_cal_callback, DialogCalendar

from app import dp, bot
from keyboards import *
from states import CreateGiveStates
from database import GiveAway, ChatRoom, Admin


@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def add_chatroom(message: types.Message):
    chat_id = message.chat.id
    chatroom = await ChatRoom.get_or_none(chat_id=chat_id)
    if chatroom:
        print(f'Chatroom {chatroom.chat_id} already exists')
        message_text = f'Добро пожаловать в чат, {message.from_user.first_name}! Менеджер уведомлен о вашем входе и скоро свяжется с вами.'
        await bot.send_message(chat_id=chat_id, text=message_text)
        for admin in await Admin.all():
            await bot.send_message(chat_id=admin.telegram_id, text=f'Пользователь @{message.from_user.username} вошел в соответсвующий чат и ожидает связи с менеджером')
        return
    chatroom = await ChatRoom.create(chat_id=chat_id)
    print(f'Chatroom {chatroom.chat_id} created')


