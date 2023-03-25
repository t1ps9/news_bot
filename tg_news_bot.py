import asyncio
from telethon import TelegramClient
from telethon.tl import functions, types
from telethon import functions, types
from telethon.tl.functions.messages import GetHistoryRequest
import time
from threading import Thread
from asyncio import set_event_loop, new_event_loop
from collections import defaultdict
from telethon import TelegramClient, Button, events, sync
from telegraph import Telegraph
from telegraph.utils import html_to_content
telegraph = Telegraph('*')
account = telegraph.create_account(short_name='216')

import datetime
import pytz
import time

utc = pytz.UTC


api_id = 0
api_hash = '*'

phone = '*'
TOKEN = '*'

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=TOKEN)
client = TelegramClient(phone, api_id, api_hash)
client.start()

ch_array = ['https://telegram.me/ru3dnews',
            'https://t.me/rozetked',
            'https://t.me/trashbox_feed',
            'https://t.me/htech_plus',
            'https://t.me/iphonesru',
            'https://t.me/techsparks',
            'https://t.me/xakep_ru']
ch_id_to_url = {1007302005: 'https://t.me/rozetked',
                1065865491: 'https://telegram.me/ru3dnews',
                1111063013: 'https://t.me/trashbox_feed',
                1158411788: 'https://t.me/htech_plus',
                1002500850: 'https://t.me/iphonesru',
                1009962628: 'https://t.me/techsparks',
                1034068795: 'https://t.me/xakep_ru'}

channel_list = [
    [
        Button.inline("❌ ru3dnews", b"chl1")
    ],
    [
        Button.inline("❌ rozetked", b"chl2")
    ],
    [
        Button.inline("❌ trashbox_feed", b"chl3")
    ],
    [
        Button.inline("❌ htech_plus", b"chl4")
    ],
    [
        Button.inline("❌ iphonesru", b"chl5")
    ],
    [
        Button.inline("❌ techsparks", b"chl6")
    ],
    [
        Button.inline("❌ xakep_ru", b"chl7")
    ],
    [
        Button.inline("👈🏿 Назад", b"chl8")
    ]
]

def negative(button):
    if button.text[0] == '✅':
        button.text = '❌' + button.text[1:]
    else:
        button.text = '✅' + button.text[1:]
    return button


@bot.on(events.NewMessage(pattern='/start'))
async def hello_message(message):
    global cnt_news
    cnt_news = defaultdict()
    global date
    date = defaultdict()
    global chan
    chan = defaultdict()
    channel_list[0][0] = Button.inline("❌ ru3dnews", b"chl1")
    channel_list[1][0] = Button.inline("❌ rozetked", b"chl2")
    channel_list[2][0] = Button.inline("❌ trashbox_feed", b"chl3")
    channel_list[3][0] = Button.inline("❌ htech_plus", b"chl4")
    channel_list[4][0] = Button.inline("❌ iphonesru", b"chl5")
    channel_list[5][0] = Button.inline("❌ techsparks", b"chl6")
    channel_list[6][0] = Button.inline("❌ xakep_ru", b"chl7")
    keyboard = [
        [
            Button.inline("Число новостей", b"main1"),
            Button.inline("Список каналов", b"main2")
        ],
        [
            Button.inline("Срок парсинга", b"main3"),
            Button.inline("Запарсить", b"main4")
        ],
    ]
    await bot.send_message(message.chat_id, "Настроить парсинг:", buttons=keyboard)

@bot.on(events.InlineQuery(pattern=""))
async def handler(event):
    global cnt_news
    cnt_news = defaultdict()
    global date
    date = defaultdict()
    global chan
    chan = defaultdict()
    channel_list[0][0] = Button.inline("❌ ru3dnews", b"chl1")
    channel_list[1][0] = Button.inline("❌ rozetked", b"chl2")
    channel_list[2][0] = Button.inline("❌ trashbox_feed", b"chl3")
    channel_list[3][0] = Button.inline("❌ htech_plus", b"chl4")
    channel_list[4][0] = Button.inline("❌ iphonesru", b"chl5")
    channel_list[5][0] = Button.inline("❌ techsparks", b"chl6")
    channel_list[6][0] = Button.inline("❌ xakep_ru", b"chl7")
    chan.update({'ru3dnews': 'https://telegram.me/ru3dnews'})
    chan.update({'rozetked': 'https://t.me/rozetked'})
    chan.update({'trashbox_feed': 'https://t.me/trashbox_feed'})
    chan.update({'htech_plus': 'https://t.me/htech_plus'})
    chan.update({'iphonesru': 'https://t.me/iphonesru'})
    chan.update({'techsparks': 'https://t.me/techsparks'})
    chan.update({'xakep_ru': 'https://t.me/xakep_ru'})
    cnt_news.update({'количество каналов': 10})
    date.update({'1 неделя': 1})
    day_diff = 7
    res = 0
    res_news = list(cnt_news.values())[0]
    date_res = list(date.keys())[0]
    name_chan = ', '.join('{}'.format(key) for key in chan.keys())
    chan_res = ', '.join('{}'.format(value) for value in chan.values())
    len_chan = len(chan.values())
    list_chan = ' '.join('{}'.format(value) for value in chan.values()).split()
    req_messages = []
    for i in range(len_chan):
        channel = await client.get_entity(list_chan[i])
        messages = await client.get_messages(channel, limit=50)

        start_day = datetime.datetime.today()
        end_day = start_day - datetime.timedelta(days=day_diff)
        for el in messages:
            if el.date.replace(tzinfo=utc) <= start_day.replace(tzinfo=utc) and el.date.replace(
                    tzinfo=utc) >= end_day.replace(tzinfo=utc):
                req_messages.append(el)
                res += 1
    # начало метрики
    top_messages = []  # топ сообщений
    good_emotions = ['👍', '❤️', '🔥', '👌', '❤️‍🔥', '🤩', '😍']
    for elem in req_messages:
        emotions = 0
        constan = 0.5
        if elem.peer_id.channel_id == 1111063013 or elem.peer_id.channel_id == 1158411788:
            constan = 2
        elif elem.peer_id.channel_id == 1065865491 or elem.peer_id.channel_id == 1007302005:
            constan = 1
        if elem.reactions is not None:
            for react in elem.reactions.results:
                if react.reaction.emoticon in good_emotions:
                    emotions += react.count
        metric = (emotions) / (constan * elem.views)
        tup_elem = (elem, metric)
        top_messages.append(tup_elem)
    top_messages.sort(key=lambda tup: tup[1], reverse=True)
    top_messages = top_messages[:list(cnt_news.values())[0]]
    html_string = ""
    counter_for_cycle = 0
    for element in top_messages:
        counter_for_cycle += 1
        html_string += '<h1>' + str(counter_for_cycle) + ': ' + '<a href=' + ch_id_to_url[
            element[0].peer_id.channel_id] + '/' + str(
            element[0].id) + ">Ссылка на оригинал новости в канале</a>" + '</h1>' + '\n\n'
        html_string += '<h1>' + element[0].text + '</h2>' + '\n\n'
    content = html_to_content(html_string)
    new_page = telegraph.create_page(title="Formed Digest", content=content)
    keyboard = event.builder.article(title="Быстрый дайджест", text=new_page[1])
    await event.answer([keyboard])

@bot.on(events.CallbackQuery)
async def callback_q(event):
    global chan_res
    global res_news
    global len_chan
    global list_chan
    global day_diff
    keyboard = [
        [
            Button.inline("Число новостей", b"main1"),
            Button.inline("Список каналов", b"main2")
        ],
        [
            Button.inline("Срок парсинга", b"main3"),
            Button.inline("Запарсить", b"main4")
        ],
    ]
    cnt_menu = [
        [
            Button.inline("1", b"cnt1"),
            Button.inline("3", b"cnt2")
        ],
        [
            Button.inline("5", b"cnt3"),
            Button.inline("10", b"cnt4")
        ]
    ]

    data_list = [
        [
            Button.inline("1 день", b"date1"),
            Button.inline("3 дня", b"date2")
        ],
        [
            Button.inline("1 неделя", b"date3"),
            Button.inline("1 месяц", b"date4")
        ]
    ]
    if event.data == b"main1":
        await bot.edit_message(event.chat_id, event.message_id, "Число новостей:", buttons=cnt_menu)

    if event.data == b"main2":
        await bot.edit_message(event.chat_id, event.message_id, "Список каналов:", buttons=channel_list)

    if event.data == b"main3":
        await bot.edit_message(event.chat_id, event.message_id, "Срок парсинга:", buttons=data_list)

    if event.data == b"chl1":
        channel_list[0][0] = negative(channel_list[0][0])
        await bot.edit_message(event.chat_id, event.message_id, "Список каналов:", buttons=channel_list)
        if 'ru3dnews' in chan:
            chan.pop('ru3dnews')
        else:
            chan.update({'ru3dnews': 'https://telegram.me/ru3dnews'})

    if event.data == b"chl2":
        channel_list[1][0] = negative(channel_list[1][0])
        await bot.edit_message(event.chat_id, event.message_id, "Список каналов:", buttons=channel_list)
        if 'rozetked' in chan:
            chan.pop('rozetked')
        else:
            chan.update({'rozetked': 'https://t.me/rozetked'})

    if event.data == b"chl3":
        channel_list[2][0] = negative(channel_list[2][0])
        await bot.edit_message(event.chat_id, event.message_id, "Список каналов:", buttons=channel_list)
        if 'trashbox_feed' in chan:
            chan.pop('trashbox_feed')
        else:
            chan.update({'trashbox_feed': 'https://t.me/trashbox_feed'})

    if event.data == b"chl4":
        channel_list[3][0] = negative(channel_list[3][0])

        await bot.edit_message(event.chat_id, event.message_id, "Список каналов:", buttons=channel_list)
        if 'htech_plus' in chan:
            chan.pop('htech_plus')
        else:
            chan.update({'htech_plus': 'https://t.me/htech_plus'})

    if event.data == b"chl5":
        channel_list[4][0] = negative(channel_list[4][0])

        await bot.edit_message(event.chat_id, event.message_id, "Список каналов:", buttons=channel_list)
        if 'iphonesru' in chan:
            chan.pop('iphonesru')
        else:
            chan.update({'iphonesru': 'https://t.me/iphonesru'})

    if event.data == b"chl6":
        channel_list[5][0] = negative(channel_list[5][0])

        await bot.edit_message(event.chat_id, event.message_id, "Список каналов:", buttons=channel_list)
        if 'techsparks' in chan:
            chan.pop('techsparks')
        else:
            chan.update({'techsparks': 'https://t.me/techsparks'})

    if event.data == b"chl7":
        channel_list[6][0] = negative(channel_list[6][0])

        await bot.edit_message(event.chat_id, event.message_id, "Список каналов:", buttons=channel_list)
        if 'xakep_ru' in chan:
            chan.pop('xakep_ru')
        else:
            chan.update({'xakep_ru': 'https://t.me/xakep_ru'})

    if event.data == b"chl8":
        await bot.edit_message(event.chat_id, event.message_id, "Настроить парсинг:", buttons=keyboard)

    if event.data == b"cnt1":
        await bot.edit_message(event.chat_id, event.message_id, "Настроить парсинг:", buttons=keyboard)
        cnt_news.clear()
        cnt_news.update({'количество каналов': 1})

    if event.data == b"cnt2":
        await bot.edit_message(event.chat_id, event.message_id, "Настроить парсинг:", buttons=keyboard)
        cnt_news.clear()
        cnt_news.update({'количество каналов': 3})

    if event.data == b"cnt3":
        await bot.edit_message(event.chat_id, event.message_id, "Настроить парсинг:", buttons=keyboard)
        cnt_news.clear()
        cnt_news.update({'количество каналов': 5})

    if event.data == b"cnt4":
        await bot.edit_message(event.chat_id, event.message_id, "Настроить парсинг:", buttons=keyboard)
        cnt_news.clear()
        cnt_news.update({'количество каналов': 10})

    if event.data == b"date1":
        await bot.edit_message(event.chat_id, event.message_id, "Настроить парсинг:", buttons=keyboard)
        date.clear()
        date.update({'1 день': 1})
        day_diff = 1

    if event.data == b"date2":
        await bot.edit_message(event.chat_id, event.message_id, "Настроить парсинг:", buttons=keyboard)
        date.clear()
        date.update({'3 дня': 1})
        day_diff = 3

    if event.data == b"date3":
        await bot.edit_message(event.chat_id, event.message_id, "Настроить парсинг:", buttons=keyboard)
        date.clear()
        date.update({'1 неделя': 1})
        day_diff = 7

    if event.data == b"date4":
        await bot.edit_message(event.chat_id, event.message_id, "Настроить парсинг:", buttons=keyboard)
        date.clear()
        date.update({'1 месяц': 1})
        day_diff = 30

    if event.data == b"main4":
        await bot.delete_messages(event.chat_id, event.message_id)
        try:
            await bot.send_message(event.chat_id, "Запарсилось, пропишите /res , чтобы посмотреть, что есть")
            res_news = list(cnt_news.values())[0]
            date_res = list(date.keys())[0]
            name_chan = ', '.join('{}'.format(key) for key in chan.keys())
            chan_res = ', '.join('{}'.format(value) for value in chan.values())
            len_chan = len(chan.values())
            list_chan = ' '.join('{}'.format(value) for value in chan.values()).split()
            await bot.send_message(event.chat_id, f'Количество новостей: {res_news}')
            await bot.send_message(event.chat_id, f'Срок: {date_res}')
            await bot.send_message(event.chat_id, f'Каналы, которые вы выбрали: {name_chan}')
        except:
            await bot.send_message(event.chat_id, "Что-то не так, ничего нет!")


req_messages = []  # здесь объекты из парсилки, которые подходят по требованиям


@bot.on(events.NewMessage(pattern='/res'))
async def cat(message):
    res = 0
    req_messages = []
    for i in range(len_chan):
        channel = await client.get_entity(list_chan[i])
        messages = await client.get_messages(channel, limit=50)

        start_day = datetime.datetime.today()
        end_day = start_day - datetime.timedelta(days=day_diff)

        for el in messages:
            if el.date.replace(tzinfo=utc) <= start_day.replace(tzinfo=utc) and el.date.replace(
                    tzinfo=utc) >= end_day.replace(tzinfo=utc):
                req_messages.append(el)
                res += 1
    if res == 0:
        await bot.send_message(message.chat.id, "ничего нет(")
    # начало метрики
    top_messages = []  # топ сообщений
    good_emotions = ['👍', '❤️', '🔥', '👌', '❤️‍🔥', '🤩', '😍']
    for elem in req_messages:
        emotions = 0
        constan = 0.5
        if elem.peer_id.channel_id == 1111063013 or elem.peer_id.channel_id == 1158411788:
            constan = 3
        elif elem.peer_id.channel_id == 1065865491 or elem.peer_id.channel_id == 1007302005:
            constan = 1
        if elem.reactions is not None:
            for react in elem.reactions.results:
                if react.reaction.emoticon in good_emotions:
                    emotions += react.count
        metric = (emotions) / (constan * elem.views)
        tup_elem = (elem, metric)
        top_messages.append(tup_elem)
    top_messages.sort(key=lambda tup: tup[1], reverse=True)
    top_messages = top_messages[:list(cnt_news.values())[0]]
    html_string = ""
    counter_for_cycle = 0
    for element in top_messages:
        counter_for_cycle += 1
        html_string += '<h1>' + str(counter_for_cycle) + ': ' + '<a href=' + ch_id_to_url[element[0].peer_id.channel_id] + '/' + str(
            element[0].id) + ">Ссылка на оригинал новости в канале</a>" + '</h1>' + '\n\n'
        html_string += '<h1>' + element[0].text + '</h2>' + '\n\n'
    content = html_to_content(html_string)
    new_page = telegraph.create_page(title="Formed Digest", content=content)
    await bot.send_message(message.chat.id, new_page[1])


bot.run_until_disconnected()
