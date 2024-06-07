import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import CantParseEntities
from aiogram_calendar import dialog_cal_callback, DialogCalendar
from database.models import ChatRoom, Participant, Message, Admin
from states.admin import ChatState
from app import dp, bot
from keyboards import *


@dp.callback_query_handler(
    text=bt_admin_help.callback_data
)
async def help(jam: types.CallbackQuery):

    await jam.message.edit_text(
        text='''Что бы вы хотели сделать?''',
        reply_markup=kb_admin_help_menu
    )


@dp.callback_query_handler(
    text=bt_admin_create_give_help.callback_data,
)
async def create_give_help(jam: types.CallbackQuery):
    await bot.send_message(
        chat_id=jam.from_user.id,
        text='''Для того, чтобы создать розыгрыш, вам необходимо выполнить следующие шаги:\n\n
1. Нажмите на кнопку "Создать розыгрыш в меню и следуйте инструкциям. После создания розыгрыша он переходит в статус созданных розыгрышей, что означает, что он 
был создан, но не активирован и не будет сразу доступен для участия.'''
    )
    with open('help_videos/create_giveaway.mov', 'rb') as video:
        await bot.send_video(
            chat_id=jam.from_user.id,
            video=video
        )


@dp.callback_query_handler(
    text=bt_admin_created_gives_help.callback_data,
)
async def created_gives_help(jam: types.CallbackQuery):
    await bot.send_message(
        chat_id=jam.from_user.id,
        text='''Для того, чтобы управлять созданными розыгрышами, вам необходимо выполнить следующие шаги:\n\n
1. Нажмите на кнопку "Созданные розыгрыши" в меню и выберите розыгрыш, которым хотите управлять. После выбора розыгрыша, вам будут доступны действия, которые вы можете совершить с ним:\n
- Добавить каналы для созданного розыгрыша\n
- Активировать розыгрыш\n
- Удалить розыгрыш\n
2. Чтобы добавить каналы для созданного розыгрыша, нажмите на кнопку "Каналы" и "Добавить каналы". После этого вам нужно будет перенаправить сообщение с каналов, которые вы хотите добавить к розыгрышу. 
Обратите внимание, что вы можете добавить только каналы, в которых бот является администратором. При этом существует два вида каналов:\n
1) Каналы, в которых будут публиковаться сообщения о розыгрыше и на которые обязательно должны быть подписаны участники розыгрыша\n
2) Каналы, в которых не будут публиковаться сообщения о розыгрыше и на которые обязательно должны быть подписаны участники розыгрыша\n\n
Для того, чтобы добавить первый тип каналов, вам необходимо, чтобы бот был администратором в соответствующем канале со следующими правами:\n
- публикация сообщений\n
- редактирование чужих публикаций\n\n
Для того, чтобы добавить второй тип каналов, вам необходимо, чтобы бот был администратором без каких-либо прав в соответствующем канале.\n\n
Для удаления каналов из розыгрыша, нажмите на кнопку "Подключенные каналы", выбирите каналы, которые вы хотите удалить и нажмите на кнопку "Удалить каналы". Таким же образом можно просматривать список подключенных каналов\n\n'''
    )
    with open('help_videos/channels.mov', 'rb') as video:
        await bot.send_video(
            chat_id=jam.from_user.id,
            video=video
        )


@dp.callback_query_handler(
    text=bt_admin_started_gives_help.callback_data,
)
async def started_gives_help(jam: types.CallbackQuery):
    await bot.send_message(
        chat_id=jam.from_user.id,
        text='''Для того, чтобы активировать розыгрыш, вам необходимо выполнить следующие шаги:\n\n
        1. Нажмите на кнопку "Созданные розыгрыши" в меню и выберите розыгрыш, который вы хотите активировать. После выбора розыгрыша, нажмите на кнопку "Активировать розыгрыш". После этого розыгрыш станет доступен для участия участников и будет опубликован в соответствующих каналах. Обратите внимание, что после активации розыгрыша вы не сможете его удалить или изменить - только остановить.\n\n'''
    )
    with open('help_videos/activate_giveaway.mov', 'rb') as video:
        await bot.send_video(
            chat_id=jam.from_user.id,
            video=video
        )


@dp.callback_query_handler(
    text=bt_admin_executed_gives_help.callback_data,
)
async def executed_gives_help(jam: types.CallbackQuery):
    await bot.send_message(
        chat_id=jam.from_user.id,
        text='''Для того, чтобы начать розыгрыш призов, вам необходимо выполнить следующие шаги:\n\n
        1. Нажмите на кнопку "Активные розыгрыши" в меню и выберите розыгрыш, который вы хотите начать. После выбора розыгрыша, нажмите на кнопку "Запустить розыгрыш". После этого розыгрыш будет завершен и победители будут выбраны. Сразу после этого произойдет розыгрыш призов и будет определен победитель (победители)\n\n'''
    )
    with open('help_videos/start_giveaway.mov', 'rb') as video:
        await bot.send_video(
            chat_id=jam.from_user.id,
            video=video
        )

@dp.callback_query_handler(
    text=bt_admin_active_chat_help.callback_data,
)
async def active_chat_help(jam: types.CallbackQuery):
    await bot.send_message(
        chat_id=jam.from_user.id,
        text='''Для того, чтобы связаться с победителем, вам необходимо выполнить следующие шаги:\n\n
        1. Нажмите на кнопку "Завершенные розыгрыши" в меню и выберите розыгрыш, победителя которого вы хотите найти. После выбора розыгрыша, нажмите на кнопку "Выбрать победителя". После этого вам будет доступен список участников розыгрыша, из которого вы можете выбрать нужного вам победителя. После выбора победителя, нажмите на кнопку "Сделать чат активным". После этого вы сможете нажать в меню кнопку "Перейти к активной беседе" и начать общение с победителем. Обращаем внимание на то, что сообщения, направляемые боту будут перенаправлены в чат с победителем только в том случае, если кнопка "Перейти к активной беседе" была нажата\n\n'''
    )
    with open('help_videos/contact_winner.mov', 'rb') as video:
        await bot.send_video(
            chat_id=jam.from_user.id,
            video=video
        )


@dp.callback_query_handler(
    text=bt_admin_lifecycle_help.callback_data,
)
async def lifecycle_help(jam: types.CallbackQuery):
    await bot.send_message(
        chat_id=jam.from_user.id,
        text='''Для того, чтобы узнать жизненный цикл розыгрыша, вам необходимо выполнить следующие шаги:\n\n
        1. Розыгрыш проходит следующие стадии:\n
        - Создание розыгрыша\n
        - Активация розыгрыша\n
        - Проведение розыгрыша\n
        - Связь с победителем\n

        2. После создания розыгрыша, он переходит в статус "Созданные розыгрыши". В этом статусе вы можете добавить каналы для розыгрыша, активировать его или удалить, но он не доступен для участия участников и не публикуется в каналах\n
        3. После активации розыгрыша, он переходит в статус "Активные розыгрыши". В этом статусе розыгрыш доступен для участия участников и публикуется в каналах\n
        4. После завершения розыгрыша, он переходит в статус "Завершенные розыгрыши". В этом статусе вы можете выбрать победителя и начать общение с ним\n\n'''
    )
