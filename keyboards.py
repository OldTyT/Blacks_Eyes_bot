from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_help = KeyboardButton('🆘Помощь')
button_donate = KeyboardButton('💰Поблагодарить')
button_remove = KeyboardButton('🗑Убрать клавиатуру')
button_profile = KeyboardButton('👤Профиль')
button_location = KeyboardButton('Отправить свою локацию 🗺️', request_location=True)

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
greet_kb.row(button_profile)
greet_kb.row(button_help)
greet_kb.add(button_donate)
greet_kb.add(button_location)
greet_kb.add(button_remove)

markup5 = ReplyKeyboardMarkup().row(
    button_profile, button_help
).add(button_location)

markup5.row(button_remove, button_donate)

#########################

inline_btn_1 = InlineKeyboardButton('Получить фотографии автомобиля', callback_data='photoAuto')
inline_btn_2 = InlineKeyboardButton('Отчет об автомобиле по гос номеру', callback_data='autoCheckGosNumber')
inline_kb_auto = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
inline_kb_auto.add(inline_btn_2)
inline_kb_TEST = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('TEST', callback_data='TEST'))