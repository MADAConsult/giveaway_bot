from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .cancel_action import bt_admin_cancel_action


bt_admin_winners = InlineKeyboardButton('Посмотреть победителей', callback_data='admin_show_statistic')

kb_admin_executed_gives = InlineKeyboardMarkup().add(bt_admin_winners).add(bt_admin_cancel_action)
