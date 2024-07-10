from aiogram import types
from aiogram.dispatcher import FSMContext

from app import dp
from keyboards import kb_admin_menu
from .admin.functions_for_active_gives.handle_new_members_from_button_giveaways import manage_new_members_from_button_gives
from .admin.functions_for_active_gives.check_channels_subscriptions import check_channels_subscriptions
from database import TemporaryUsers, GiveAwayStatistic, Participant, Admin, GiveAway
from config import start_text, OWNERS


@dp.message_handler(
    commands=['start'],
    state='*'
)
async def process_start(jam: types.Message, state: FSMContext):
    await state.finish()


    if ' ' in jam.text:
        give_callback_value = jam.text.split(' ')[1]

        if '=watchresult' in give_callback_value:
            give_callback_value = give_callback_value.split('=')[0]

            await TemporaryUsers().add_user(
                callback_value=give_callback_value,
                new_member_id=jam.from_user.id,
                new_member_username=jam.from_user.username
            )
            
            stats = await GiveAwayStatistic().get(giveaway_callback_value=give_callback_value)
            winner_count = await stats.winners.all().count()
            if winner_count == 0:

                await jam.answer(
                    '💎  <b>Вы подписались на результаты розыгрыша, ожидайте!</b>',
                )
            
            else:
                await jam.answer(
                    '💎  <b>Результаты розыгрыша уже опубликованы!</b>',
                )


        elif '=getresults' in give_callback_value:
            give_callback_value = give_callback_value.split('=')[0]

            winners_data = await GiveAwayStatistic().get(
                giveaway_callback_value=give_callback_value
            )
            winners_data = await winners_data.winners.all()
            print(winners_data)

            text = "💎  <b>Результаты розыгрыша:</b>\n\n"
            for user_info in winners_data:
                text += f"@{user_info.username}\n"
            await jam.answer(text=text)



        else:
            if await check_channels_subscriptions(
                    give_callback_value=give_callback_value,
                    user_id=jam.from_user.id
            ):

                await manage_new_members_from_button_gives(
                    jam=jam,
                    state=state,
                    give_callback_value=give_callback_value
                )

            else:
                await jam.answer(
                    '💎  <b>Вы не подписаны на все каналы!</b>'
                )

    else:
        admins = await Admin.all()
        for admin in admins:
            if jam.from_user.id != admin.telegram_id:
                continue
            else:
                break
        else:
            return
        await state.finish()
        await jam.answer(
            start_text,
            reply_markup=kb_admin_menu
        )
