from aiogram import types
from aiogram.dispatcher import FSMContext
from app import dp
from database import GiveAwayStatistic, GiveAway
from keyboards import *
from states import ExecutedGivesStates

@dp.callback_query_handler(
    text=bt_admin_executed_gives.callback_data,
    state='*'
)
async def execute_giveaway(
    jam: types.CallbackQuery,
    state: FSMContext
):
    markup = await GiveAway().get_give_data_for_executed_give(
        user_id=jam.from_user.id
    )

    if markup:
        markup.add(bt_admin_cancel_action)
        await ExecutedGivesStates.select_give.set()
        await jam.message.edit_text(
            text='Выберите розыгрыш',
            reply_markup=markup
        )
    else:
        await jam.answer(
            text='У вас нет завершенных розыгрышей',
        )
        