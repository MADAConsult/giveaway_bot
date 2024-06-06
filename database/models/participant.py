from datetime import datetime, timedelta
from typing import NamedTuple

from tortoise import Model, fields

from config import timezone_info


class Participant(Model):
    telegram_id = fields.BigIntField(pk=True)
    username = fields.TextField(null=True)
    first_name = fields.TextField(null=True)
    last_name = fields.TextField(null=True)
    join_date = fields.DatetimeField(auto_now_add=True)


class GiveAwayStatistic_Participant(Model):
    id = fields.BigIntField(pk=True)
    is_winner = fields.BooleanField(default=False)
