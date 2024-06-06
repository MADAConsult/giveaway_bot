from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


bt_admin_create_give = InlineKeyboardButton('Создать розыгрыш', callback_data='admin_gives')
bt_admin_created_gives = InlineKeyboardButton('Созданные розыгрыши', callback_data='admin_created_gives')
bt_admin_started_gives = InlineKeyboardButton('Активные розыгрыши', callback_data='admin_started_gives')
bt_admin_executed_gives = InlineKeyboardButton('Завершенные розыгрыши', callback_data='admin_executed_gives')
bt_admin_active_chat = InlineKeyboardButton('Перейти к активной беседе', callback_data='admin_active_chat')

kb_admin_menu = InlineKeyboardMarkup().add(bt_admin_create_give, bt_admin_created_gives).add(bt_admin_started_gives).add(bt_admin_executed_gives).add(bt_admin_active_chat)
