from database import GiveAway, TelegramChannel, GiveAwayStatistic, Participant
from .winners_animation import run_winners_animation



async def process_end_of_giveaway(
        give_callback_value: str,
        owner_id: int
):
    winners_data = await GiveAway().filter(callback_value=give_callback_value).all().values('winners_count')
    channels_data = await TelegramChannel().get_channel_data(owner_id=owner_id)
    statistic_data = await GiveAwayStatistic().filter(giveaway_callback_value=give_callback_value).all()
    members = await Participant().filter(giveaway_statistic__giveaway_callback_value=give_callback_value).all()

    for channel in channels_data:


        await run_winners_animation(
            give_callback_value=give_callback_value,
            channel_id=channel['channel_id'],
            members_from_giveaway=list(members),
            winners_count=winners_data[0]['winners_count'],
        )
