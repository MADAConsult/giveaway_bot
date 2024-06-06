import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import CantParseEntities
from aiogram_calendar import dialog_cal_callback, DialogCalendar
from database.models import ChatRoom, Participant, Message, Admin
from states.admin import ChatState
from app import dp, bot


@dp.message_handler()
async def message_handler_to_winners(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    from_user = await Participant.get_or_none(telegram_id=message.from_user.id)
    chatroom = await ChatRoom.get_or_none(winner=from_user)
    if chatroom is None:
        return
    from_user = await Participant.get_or_none(telegram_id=message.from_user.id)
    if from_user is None:
        print('User not found')
        return
    else:
        message = await Message.create(
            from_user=from_user,
            chat_id=chat_id,
            message_id=message.message_id,
            text=message.text,
            winner=from_user
        )
        await message.save()
    admins = await Admin.all()
    for admin in admins:
        admin_active_chat = await admin.current_winner_chat_id
        if admin_active_chat == chatroom:
            await bot.forward_message(chat_id=admin.telegram_id, from_chat_id=chat_id, message_id=message.message_id)



@dp.message_handler(state=ChatState.is_chatting)
async def message_handler_to_chatroom(message: types.Message, state: FSMContext):
    print('Message handler to chatroom')
    chat_id = message.chat.id
    admin = await Admin.get_or_none(telegram_id=message.from_user.id)
    if admin is None:
        return
    else:
        current_winner_chat_id = await admin.current_winner_chat_id
        if not current_winner_chat_id:
            return
        winner = await current_winner_chat_id.winner
        message = await Message.create(
            chat_id=1,
            message_id=message.message_id,
            text=message.text,
            winner=winner
        )
        await message.save()
        chat_id = winner.telegram_id
        await bot.send_message(chat_id=chat_id, text=message.text)
        await bot.send_message(chat_id=admin.telegram_id, text='Сообщение отправлено')
