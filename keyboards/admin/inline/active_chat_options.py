from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .cancel_action import bt_admin_cancel_action


bt_admin_active_chat_messages = InlineKeyboardButton('Посмотреть все сообщения', callback_data='admin_active_chat_messages')

kb_admin_active_chat = InlineKeyboardMarkup().add(bt_admin_active_chat_messages).add(bt_admin_cancel_action)