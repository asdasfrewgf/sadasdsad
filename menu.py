from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

mainkb = ReplyKeyboardMarkup(
    resize_keyboard=True,
	keyboard = [
        [
            KeyboardButton(text="💼 Личный кабинет"),
            KeyboardButton(text="📊 Мои активы")
		],
		[
            KeyboardButton(text="🔷 О сервисе"),
            KeyboardButton(text="👨🏻‍💻 Тех. поддержка")
		]
	]
)

pt2 = InlineKeyboardButton('Обновить курс', callback_data='bitcoin')
pt1 = InlineKeyboardButton('Отменить', callback_data='cancel')
btc = InlineKeyboardMarkup(row_width=1).add(pt2).add(pt1)

pt2 = InlineKeyboardButton('Обновить курс', callback_data='ethereum')
pt1 = InlineKeyboardButton('Отменить', callback_data='cancel')
eth = InlineKeyboardMarkup(row_width=1).add(pt2).add(pt1)

pt2 = InlineKeyboardButton('Обновить курс', callback_data='polkadot')
pt1 = InlineKeyboardButton('Отменить', callback_data='cancel')
dots = InlineKeyboardMarkup(row_width=1).add(pt2).add(pt1)

pt2 = InlineKeyboardButton('Обновить курс', callback_data='doge')
pt1 = InlineKeyboardButton('Отменить', callback_data='cancel')
dogec = InlineKeyboardMarkup(row_width=1).add(pt2).add(pt1)

pt2 = InlineKeyboardButton('Обновить курс', callback_data='ripple')
pt1 = InlineKeyboardButton('Отменить', callback_data='cancel')
ripples = InlineKeyboardMarkup(row_width=1).add(pt2).add(pt1)

pt2 = InlineKeyboardButton('Обновить курс', callback_data='litecoin')
pt1 = InlineKeyboardButton('Отменить', callback_data='cancel')
lites = InlineKeyboardMarkup(row_width=1).add(pt2).add(pt1)

pt2 = InlineKeyboardButton('Обновить курс', callback_data='solana')
pt1 = InlineKeyboardButton('Отменить', callback_data='cancel')
sola = InlineKeyboardMarkup(row_width=1).add(pt2).add(pt1)

pt2 = InlineKeyboardButton('Обновить курс', callback_data='tron')
pt1 = InlineKeyboardButton('Отменить', callback_data='cancel')
trons = InlineKeyboardMarkup(row_width=1).add(pt2).add(pt1)

pt2 = InlineKeyboardButton('Обновить курс', callback_data='cardano')
pt1 = InlineKeyboardButton('Отменить', callback_data='cancel')
carda = InlineKeyboardMarkup(row_width=1).add(pt2).add(pt1)

pt2 = InlineKeyboardButton('Обновить курс', callback_data='terra')
pt1 = InlineKeyboardButton('Отменить', callback_data='cancel')
luna = InlineKeyboardMarkup(row_width=1).add(pt2).add(pt1)

pt1 = InlineKeyboardButton('Отменить', callback_data='cancel')
otmena = InlineKeyboardMarkup(row_width=1).add(pt1)

pt1 = InlineKeyboardButton('✅ Принять правила', callback_data='SoglDa')
prinsogl = InlineKeyboardMarkup(row_width=1).add(pt1)

pt1 = InlineKeyboardButton('📄 Соглашение', url='https://telegra.ph/Polzovatelskoe-soglashenie-CPAnet-04-10')
pt2 = InlineKeyboardButton('Личный кабинет', callback_data='lk')
goodsogl = InlineKeyboardMarkup(row_width=1).add(pt1,pt2)

lk = InlineKeyboardMarkup(
	inline_keyboard = [
        [
            InlineKeyboardButton(text='💳 Пополнить', callback_data='popolnenie'),
            InlineKeyboardButton(text='🏦 Вывести', callback_data='vivod')
        ],
        [
            InlineKeyboardButton(text='🗃 Верификация', callback_data='verif')
		]
	]
)

verifir = InlineKeyboardMarkup(
	inline_keyboard = [
        [
            InlineKeyboardButton(text='Пройти верификацию', url='https://t.me/Xsupport_Casinobot')
		]
	]
)

tp = InlineKeyboardMarkup(
	inline_keyboard = [
        [
            InlineKeyboardButton(text='Написать', url='https://t.me/Xsupport_Casinobot')
		]
	]
)

info = InlineKeyboardMarkup(
	inline_keyboard = [
        [
            InlineKeyboardButton(text='👩‍💻 Поддержка', url='https://t.me/Xsupport_Casinobot'),
            InlineKeyboardButton(text='📄 Соглашение', url='https://telegra.ph/Polzovatelskoe-soglashenie-07-01-3')
		]
	]
)

about_me = InlineKeyboardMarkup(
    inline_keyboard= [
       [
            InlineKeyboardButton(text='📖 Условия', url='https://t.me/mdspak'),
            InlineKeyboardButton(text='📩 Тех. поддержка', url='https://t.me/mdspak')
       ],
       [
            InlineKeyboardButton(text='📈 Состояние сети', callback_data='sostoianie_seti'),
            InlineKeyboardButton(text='⚙️ Реферальная система', callback_data='referals')
       ]
    ]
)

pay = InlineKeyboardMarkup(
	inline_keyboard = [
        [
            InlineKeyboardButton(text='🥝 Киви', callback_data='qiwi_payments')
        ],
        [
            InlineKeyboardButton(text='💳 P2P перевод', callback_data='p2pcard')
		]
	]
)