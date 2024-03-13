import threading

import requests
import telebot
from telebot import types
from telebot.apihelper import _make_request

from googlesheet_reader import get_menu


class MenuBot:
    def __init__(self):
        self.bot = telebot.TeleBot('ключ бота')
        token = 'ключ бота'
        self.bot.set_webhook()

        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.bot.send_message(message.chat.id, "Добро пожаловать", reply_markup=create_menu_menu())

        @self.bot.message_handler(commands=['messages'])
        def get_messages(message):
            self.bot.send_message(message.chat.id, str(self.bot.get_updates()))

        rest_menu = get_menu()[1:]
        rest_menu_dict = {item[0]: item[2] for item in rest_menu}
        order = []
        order_location = {}

        menu_buttons = {
            "order": get_menu()
        }

        @self.bot.channel_post_handler()
        def channel_post(post):
            chat = post.chat
            chat_id = chat.id
            channels = _make_request(token=token, method_name='getUpdates')  # , params={'id': [chat_id]})
            self.bot.send_message(chat_id, "new memory: " + str(channels))

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            if call.data in rest_menu_dict.keys():
                order.append(call.data)
                text = f"Ваш заказ: {order}\n Меню: "
                self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text,
                                           reply_markup=create_menu_menu())
                return
            if call.data == "Confirm order":
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                button_geo = types.KeyboardButton(text="Отправить текущее местоположение", request_location=True)
                keyboard.add(button_geo)
                self.bot.send_message(call.message.chat.id, "Поделись местоположением", reply_markup=keyboard)
                return
            if call.data == "Approve location":
                print(order_location)
                self.bot.send_message(chat_id=call.message.chat.id,
                                      text="Предположим, оплата прошла. Заказ успешно отправлен на сервер")
                userid_header = str(call.message.from_user.id)
                order_header = str(order)
                location_header = (str(order_location["order_longitude"]) + "; " + str(order_location["order_latitude"]))
                headers = {'user': userid_header,
                           'location': location_header,
                           'order': order_header}
                requests.Request = requests.get("http://127.0.0.1:5001/process_order", headers=headers)
            if call.data == "Decline location":
                print(order_location)
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                button_geo = types.KeyboardButton(text="Отправить текущее местоположение", request_location=True)
                keyboard.add(button_geo)
                self.bot.send_message(call.message.chat.id, "Отправь верное местоположение", reply_markup=keyboard)

        @self.bot.message_handler(content_types=['location'])
        def location(message):
            if message.location is None:
                return
            print(message.location)
            order_location["order_longitude"] = message.location.longitude
            order_location["order_latitude"] = message.location.latitude
            print("METKA:", order_location["order_longitude"], type(order_location["order_longitude"]))
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(text="Approve location", callback_data="Approve location")
            markup.add(btn)
            btn2 = types.InlineKeyboardButton(text="Decline location", callback_data="Decline location")
            markup.add(btn2)
            self.bot.send_message(message.chat.id, "Указано верное местоположение?", reply_markup=markup)

        def create_menu_menu() -> types.InlineKeyboardMarkup:
            markup = types.InlineKeyboardMarkup()
            for button in rest_menu:
                price = str(button[2])
                text = f"{button[0]}: {price}"
                btn = types.InlineKeyboardButton(text=text, callback_data=button[0])
                markup.add(btn)
            btn = types.InlineKeyboardButton(text="Confirm order", callback_data="Confirm order")
            markup.add(btn)
            return markup

        def create_menu(type_menu: str) -> types.InlineKeyboardMarkup:
            markup = types.InlineKeyboardMarkup()
            for button in menu_buttons[type_menu]:
                price = str(button[2])
                text = f"{button[0]}: {price}"
                btn = types.InlineKeyboardButton(text=text, callback_data=type_menu)
                markup.add(btn)
            return markup

    def start_bot(self):
        x = threading.Thread(name="menu", target=self.bot.polling,)
        x.start()

# _make_request()
