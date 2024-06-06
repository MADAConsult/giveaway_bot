from aiogram import types
from aiogram.dispatcher import FSMContext
from app import dp
from database import GiveAwayStatistic, GiveAway
from keyboards import *
from states import ActiveGivesStates

from ..functions_for_active_gives.process_end_giveaway import process_end_of_giveaway




@dp.callback_query_handler(
    text=bt_admin_execute_give.callback_data,
    state=ActiveGivesStates.manage_selected_give
)
async def execute_giveaway(
    jam: types.CallbackQuery,
    state: FSMContext
):
    await ActiveGivesStates.stop_give.set()
    state_data = await state.get_data()
    giveaway = await GiveAway().get(
        callback_value=state_data['give_callback_value']
    )
    await process_end_of_giveaway(
        give_callback_value=state_data['give_callback_value'],
        owner_id=giveaway.owner_id
    )
