import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import CantParseEntities
from aiogram_calendar import dialog_cal_callback, DialogCalendar

from app import dp, bot
from keyboards import *
from states import CreateGiveStates, ChatState
from database import GiveAway, ChatRoom, Admin, Message


@dp.callback_query_handler(
    text=bt_admin_active_chat.callback_data
)
async def toogle_active_chat(jam: types.CallbackQuery):
    await ChatState.is_chatting.set()
    print('Active chat')
    admin = await Admin().get(telegram_id=jam.from_user.id)
    chatroom = await admin.current_winner_chat_id
    if chatroom:
        winner = await chatroom.winner
        text = f"Сейчас активен чат с пользователем {winner.username}.\nЧтобы посмотреть все сообщения, выберите победителя в соответствующем розыгрыше и нажмите кнопку 'Сделать активным'"
    else:
        text = "Активный чат не найден"
    await jam.message.edit_text(
        text=text,
        reply_markup=kb_admin_active_chat
    )


@dp.callback_query_handler(
    text=bt_admin_active_chat_messages.callback_data,
    state=ChatState.is_chatting
)
async def show_all_messages(jam: types.CallbackQuery):
    admin = await Admin().get(telegram_id=jam.from_user.id)
    chatroom = await admin.current_winner_chat_id
    if chatroom:
        winner = await chatroom.winner
        messages = await Message().filter(winner=winner)
        text = 'Чат\n'
        for message in messages:
            if message.from_user:
                text += f"👤Победитель @{winner.username}: {message.text}\n\n"
            else:
                text += f"💼Администратор: {message.text}\n\n"
    else:
        text = "Активный чат не найден"
    await jam.message.edit_text(
        text=text,
        reply_markup=kb_admin_cancel_action
    )

