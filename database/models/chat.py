import math
import random
import string
from datetime import date
from database.models.giveaway_statistic import GiveAwayStatistic

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tortoise import Model, fields


class Message(Model):
    from_user = fields.ForeignKeyField('models.Participant', related_name='from_user', null=True)
    winner = fields.ForeignKeyField('models.Participant', related_name='winner_chat', null=True)
    chat_id = fields.BigIntField()
    message_id = fields.BigIntField()
    text = fields.TextField()
    date = fields.DatetimeField(auto_now_add=True)
