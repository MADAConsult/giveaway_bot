import math
import random
import string
from datetime import date
from database.models.giveaway_statistic import GiveAwayStatistic

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tortoise import Model, fields


class ChatRoom(Model):
    winner = fields.ForeignKeyField('models.Participant', related_name='winner', null=True)
