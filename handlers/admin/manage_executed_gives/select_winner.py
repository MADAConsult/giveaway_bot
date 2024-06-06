from aiogram import types
from aiogram.dispatcher import FSMContext
from app import dp
from database import GiveAwayStatistic, GiveAway, Participant, ChatRoom
from keyboards import *
from states import ExecutedGivesStates


@dp.callback_query_handler(
    lambda c: c.data != bt_admin_cancel_action.callback_data,
    state=ExecutedGivesStates.select_winner,
)
async def execute_giveaway(
    jam: types.CallbackQuery,
    state: FSMContext
):
    await ExecutedGivesStates.winner_options.set()
    winner_id = jam.data
    user = await Participant().get(telegram_id=winner_id)
    markup = [[types.InlineKeyboardButton(text="Связаться с победителем", callback_data=f'l_{user.telegram_id}')], [bt_admin_cancel_action]]
    text = f"Победитель: {user.username}\n"
    markup.insert(1, [types.InlineKeyboardButton(text="Сделать чат активным", callback_data=f'a_{user.telegram_id}')])
    await jam.message.edit_text(
        text=text,
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=markup)
    )
