from aiogram import types
from aiogram.dispatcher import FSMContext
from app import dp, bot
from database import GiveAwayStatistic, GiveAway, Participant, ChatRoom, Admin, Message
from keyboards import *
from states import ExecutedGivesStates



@dp.callback_query_handler(
    lambda c: c.data.startswith('a_'),
    state=ExecutedGivesStates.winner_options
)
async def make_chat_active(
    jam: types.CallbackQuery,
    state: FSMContext
):
    winner_id = jam.data[2:]
    user = await Participant().get(telegram_id=winner_id)
    chat_room = await ChatRoom().get_or_none(winner=user)
    if chat_room:
        pass
    else:
        avaliable_room = ChatRoom(winner=user)
        await avaliable_room.save()
    winner_id = jam.data[2:]
    user = await Participant().get(telegram_id=winner_id)
    admin = await Admin().get(telegram_id=jam.from_user.id)
    admin.current_winner_chat_id = chat_room
    await admin.save()
    await jam.answer('Беседа с победителем активирована')