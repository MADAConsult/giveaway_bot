import asyncio
import random

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import MessageNotModified

from app import bot
from database import TemporaryUsers, GiveAwayStatistic, Participant, GiveAway

from .inform_of_the_end_give import delete_and_inform_of_the_end_give
from .check_channels_subscriptions import check_channels_subscriptions



async def create_markup_for_watch_results(
        give_callback_value: str
) -> InlineKeyboardMarkup:

    bot_data = await bot.get_me()
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            text='Присоединиться »',
            url=f'https://t.me/{bot_data.username}?start={give_callback_value}=watchresult'
        )
    )

    return markup



async def create_markup_for_watch_winners(
        give_callback_value: str
) -> InlineKeyboardMarkup:

    bot_data = await bot.get_me()
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            text='Результаты »',
            url=f'https://t.me/{bot_data.username}?start={give_callback_value}=getresults'
        )
    )

    return markup



async def run_winners_animation(
    give_callback_value: str,
    channel_id: int,
    members_from_giveaway: list,
    winners_count: int,
    winners_users: list = []
):

    """members_from_giveaway = [{'user_id': int(f'34534{i}')} for i in range(100)]
    temporary_users_usernames = []


    for i, member_info in enumerate(members_from_giveaway):
        temporary_users_usernames.append(user{i + 1}')

        member_info.update({
            'place': i + 1,
            'username': user{i + 1}'
        })"""

    summary_members_count = len(members_from_giveaway)
    print('summary_members_count:', summary_members_count)
    print('winners_count:', winners_count)
    if len(members_from_giveaway) >= winners_count:

        for member in members_from_giveaway:
            if not await check_channels_subscriptions(
                give_callback_value=give_callback_value,
                user_id=member.telegram_id
            ):
                members_from_giveaway.remove(member)
        
        try:
            winners_users = random.sample(members_from_giveaway, winners_count)
        except ValueError:
            try:
                await bot.send_message(
                    chat_id=channel_id,
                    text=f'<b>🚫  Розыгрыш завершен, победителей выбрать не удалось, участников слишком мало</b>',
                )
            except Exception as e:
                print(e)

            await delete_and_inform_of_the_end_give(
                give_callback_value=give_callback_value,
                winners=winners_users,
                summary_count_users=summary_members_count
            )
            return
        print('winners_users:', winners_users)

        stats = await GiveAwayStatistic().filter(
            giveaway_callback_value=give_callback_value
        ).first()

        giveaway = await GiveAway().get(callback_value=give_callback_value)

        print(f"before: {await stats.winners.all()}")
        for winner in winners_users:
            print('winner:', winner)
            await stats.winners.add(winner)
        print(f"after: {await stats.winners.all()}")


        markup = await create_markup_for_watch_winners(give_callback_value)
        try:
            await bot.send_message(
                chat_id=channel_id,
                text=f'<b>Розыгрыш {giveaway.name} завершен! Ожидайте оглашение списка победителей менеджером ✅</b>'
            )
        except Exception as e:
            print(e)


    else:
        try:
            await bot.send_message(
                chat_id=channel_id,
                text=f'<b>🚫  Розыгрыш завершен, победителей выбрать не удалось, участников слишком мало</b>',
            )
        except Exception as e:
            print(e)


    await delete_and_inform_of_the_end_give(
        give_callback_value=give_callback_value,
        winners=winners_users,
        summary_count_users=summary_members_count
    )
