from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .cancel_action import bt_admin_cancel_action


bt_admin_create_give_help = InlineKeyboardButton('Создать розыгрыш', callback_data='admin_gives_help')
bt_admin_created_gives_help = InlineKeyboardButton('Добаваить каналы для созданного розыгрыша', callback_data='admin_created_gives_help')
# активировать розыгрыш
bt_admin_started_gives_help = InlineKeyboardButton('Активировать розыгрыш', callback_data='admin_started_gives_help')
# начать розыгрыщ призов
bt_admin_executed_gives_help = InlineKeyboardButton('Начать розыгрыш призов', callback_data='admin_executed_gives_help')
# связаться с победителем
bt_admin_active_chat_help = InlineKeyboardButton('Связаться с победителем', callback_data='admin_active_chat_help')
# жизненный цикл розыгрыша
bt_admin_lifecycle_help = InlineKeyboardButton('Жизненный цикл розыгрыша', callback_data='admin_lifecycle_help')

kb_admin_help_menu = InlineKeyboardMarkup().add(bt_admin_create_give_help).add(bt_admin_created_gives_help).add(bt_admin_started_gives_help).add(bt_admin_executed_gives_help).add(bt_admin_active_chat_help).add(bt_admin_lifecycle_help).add().add(bt_admin_cancel_action)
