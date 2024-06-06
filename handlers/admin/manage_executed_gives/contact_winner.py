from aiogram import types
from aiogram.dispatcher import FSMContext
from app import dp, bot
from database import GiveAwayStatistic, GiveAway, Participant, ChatRoom, Admin, Message
from keyboards import *
from states import ExecutedGivesStates


@dp.callback_query_handler(
    lambda c: c.data.startswith('l_'),
    state=ExecutedGivesStates.winner_options
)
async def execute_giveaway(
    jam: types.CallbackQuery,
    state: FSMContext
):
    winner_id = jam.data[2:]
    markup = [bt_admin_cancel_action]
    user = await Participant().get(telegram_id=winner_id)
    chat_room = await ChatRoom().get_or_none(winner=user)
    text = f"Чат для связи с победителем: {user.username} активирован\n"
    if chat_room:
        pass
    else:
        avaliable_room = ChatRoom(winner=user)
        await avaliable_room.save()

    await bot.send_message(
        chat_id=user.telegram_id,
        text=f"Поздравляем, вы победили в розыгрыше! Менеджер свяжется с вами в ближайшее время через этот чат, ожидайте."
    )
    await jam.message.edit_text(
        text=text,
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[markup])
    )



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
    admin = await Admin().get(telegram_id=jam.from_user.id)
    messages = await Message().filter(winner=user)
    admin.current_winner_chat_id = chat_room
    await admin.save()
    await jam.answer('Беседа с победителем активирована')