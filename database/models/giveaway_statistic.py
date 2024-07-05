from datetime import datetime, timedelta
from typing import NamedTuple

from tortoise import Model, fields

from config import timezone_info

from .participant import Participant


class GiveAwayStatisticInfo(NamedTuple):
    count_members_in_24_hours: int
    count_members_summary: int

class GiveawayStatisticMember(Model):
    giveaway_statistic = fields.ForeignKeyField('models.GiveAwayStatistic', related_name='giveaway_statistic_members')
    participant = fields.ForeignKeyField('models.Participant', related_name='member_giveaways', to_field='telegram_id', on_delete=fields.CASCADE)

class GiveawayStatisticWinner(Model):
    giveaway_statistic = fields.ForeignKeyField('models.GiveAwayStatistic', related_name='giveaway_statistic_winners')
    participant = fields.ForeignKeyField('models.Participant', related_name='winner_giveaways', to_field='telegram_id', on_delete=fields.CASCADE)

class GiveAwayStatistic(Model):
    giveaway_callback_value = fields.TextField(pk=True)
    members = fields.ManyToManyField('models.Participant', related_name='giveaway_statistic', through='models.GiveawayStatisticMember')
    post_link = fields.TextField()
    winners = fields.ManyToManyField('models.Participant', related_name='giveaway_winners', through='models.GiveawayStatisticWinner')

    def __str__(self):
        return self.giveaway_callback_value
    

    async def add_statistic(
        self,
        giveaway_callback_value: str,
        members: list,
        winners: list,
        post_link: str,
    ):
        if not await self.exists(giveaway_callback_value=giveaway_callback_value):

            obj = await self.create(
                giveaway_callback_value=giveaway_callback_value,
                post_link=post_link
            )
            await obj.members.add(*members)


    async def delete_statistic(self, giveaway_callback_value: str):
        await self.filter(giveaway_callback_value=giveaway_callback_value).delete()



    async def exists_member(self, giveaway_callback_value: str, member_username: str) -> bool:
        stats = await self.get(giveaway_callback_value=giveaway_callback_value)
        return await stats.members.filter(username=member_username).exists()
        

    async def get_data(self, giveaway_callback_value: str) -> dict:
        data = await self.filter(
            giveaway_callback_value=giveaway_callback_value
        ).all().values('members')

        return data



    async def get_statistic(self, giveaway_callback_value: str) -> GiveAwayStatisticInfo | bool:
        data = await Participant.filter(giveaway_statistic__giveaway_callback_value=giveaway_callback_value).all()
        count_members_in_24_hours = []
        count_members_summary = []

        if data:

            for member in data:
                join_date = member.join_date

                if join_date > datetime.now(timezone_info) - timedelta(days=1):
                    count_members_in_24_hours.append(member)

                count_members_summary.append(member.username)

            return GiveAwayStatisticInfo(
                count_members_in_24_hours=len(count_members_in_24_hours),
                count_members_summary=len(count_members_summary)
            )

        else:
            return False


    async def update_statistic_members(
        self,
        giveaway_callback_value: str,
        new_member_username: str,
        new_member_id: int,
    ) -> bool:
        current_obj = await self.get(giveaway_callback_value=giveaway_callback_value)
        if await Participant.exists(telegram_id=new_member_id):
            member = await Participant.get(telegram_id=new_member_id)
            await current_obj.members.add(member)
            return False
        else:
            new_member = await Participant.create(telegram_id=new_member_id, username=new_member_username)
            await current_obj.members.add(new_member)
            return True

    
    
    async def get_all_members(self, giveaway_callback_value: str) -> list:
        data = await Participant.filter(giveaway_statistic__giveaway_callback_value=giveaway_callback_value).all()
        return data
    
    
