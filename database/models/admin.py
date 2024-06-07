
import math
import random
import string
from datetime import date
from database.models.giveaway_statistic import GiveAwayStatistic

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tortoise import Model, fields


class Admin(Model):
    telegram_id = fields.BigIntField(pk=True)
    current_winner_chat_id = fields.ForeignKeyField('models.ChatRoom', related_name='current_winner_chat_id', null=True)
