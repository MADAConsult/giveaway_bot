from aiogram import types
from aiogram.dispatcher import FSMContext
from app import dp
from database import GiveAwayStatistic, GiveAway, Participant
from keyboards import *
from states import ExecutedGivesStates


@dp.callback_query_handler(
    text=bt_admin_winners.callback_data,
    state=ExecutedGivesStates.manage_selected_give
)
async def execute_giveaway(
    jam: types.CallbackQuery,
    state: FSMContext
):
    await ExecutedGivesStates.select_winner.set()
    state_data = await state.get_data()
    stats = await GiveAwayStatistic().get(giveaway_callback_value=state_data['give_callback_value'])
    winners = await stats.winners.all()
    markup = []
    for winner in winners:
        markup.append([
            types.InlineKeyboardButton(
                text=f"{winner.username}",
                callback_data=f"{winner.telegram_id}"
            )]
        )
    markup.append([bt_admin_cancel_action])
    await jam.message.edit_text(
        text="Список победителей розыгрыша:",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=markup)
    )

