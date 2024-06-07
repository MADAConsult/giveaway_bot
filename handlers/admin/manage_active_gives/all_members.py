from aiogram import types
from aiogram.dispatcher import FSMContext
from app import dp
from database import GiveAwayStatistic
from keyboards import *
from states import ActiveGivesStates



@dp.callback_query_handler(
    text=bt_admin_all_members.callback_data,
    state=ActiveGivesStates.manage_selected_give
)
async def show_give_statistic(
    jam: types.CallbackQuery,
    state: FSMContext
):
    await ActiveGivesStates.show_statistic.set()
    state_data = await state.get_data()

    statistic_info = await GiveAwayStatistic().get_all_members(
        giveaway_callback_value=state_data['give_callback_value'])

    if statistic_info:
        message = 'Список участников:\n'
        for member in statistic_info:
            message += f'➖  <b>@{member.username}</b>\n'

        await jam.message.edit_text(
            message,
            reply_markup=kb_admin_cancel_action
        )

    else:
        await jam.answer('В розыгрыше нет участников')
