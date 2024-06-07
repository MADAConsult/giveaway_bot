from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .cancel_action import bt_admin_cancel_action


bt_admin_contact_winner = InlineKeyboardButton('Связаться с победителем', callback_data='admin_show_statistic')

bt_admin_winner_options = InlineKeyboardMarkup().add(bt_admin_contact_winner).add(bt_admin_cancel_action)
