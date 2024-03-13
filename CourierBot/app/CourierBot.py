import threading

import requests
import telebot
from telebot import types


class CourierBot:
    user_order = {}
    id: str
    order_location: str
    personal_location_str: str
    route = {}

    def __init__(self):
        self.bot = telebot.TeleBot('ключ бота')
        self.bot.set_webhook()
        self.personal_location = {}
        self.order_location = ""
        self.route = {}

        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.id = message.chat.id
            self.bot.send_message(message.chat.id, "Добро пожаловать courier bot")

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):

            if call.data == "Approve location":
                print("МАРШРУТ", self.personal_location_str, self.order_location)
                userid_header = str(call.message.from_user.id)
                location_header = self.order_location
                self.bot.send_message(chat_id=call.message.chat.id,
                                      text="Заказ принят, вычисление маршрута")
                self.route = self._route_req()
                print(self.route)
                self.bot.send_message(chat_id=call.message.chat.id,
                                      text=str(self.route))
                headers = {'user': userid_header,
                           'location': location_header}
                requests.Request = requests.get("http://127.0.0.1:5001/courier_tracking", headers=headers)

            if call.data == "Decline location":
                print(self.order_location)
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                button_geo = types.KeyboardButton(text="Отправить текущее местоположение", request_location=True)
                keyboard.add(button_geo)
                self.bot.send_message(call.message.chat.id, "Отправь верное местоположение", reply_markup=keyboard)

        @self.bot.message_handler(content_types=['location'])
        def location(message):
            if message.location is None:
                return
            print(message.location)
            self.personal_location["personal_longitude"] = message.location.longitude
            self.personal_location["personal_latitude"] = message.location.latitude
            print("METKA:", self.personal_location["personal_longitude"], type(self.personal_location["personal_longitude"]))
            self.personal_location_str = f"{self.personal_location['personal_latitude']}, {self.personal_location['personal_longitude']}"
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(text="Approve location", callback_data="Approve location")
            markup.add(btn)
            btn2 = types.InlineKeyboardButton(text="Decline location", callback_data="Decline location")
            markup.add(btn2)
            self.bot.send_message(message.chat.id, "Указано верное местоположение?", reply_markup=markup)

    def start_bot(self):
        x = threading.Thread(name="courier", target=self.bot.polling, )
        x.start()

    def order_confirmed(self):
        return self.route

    def delivery_confirm(self, location):
        location = f"{(location.split(';')[1]).strip.strip()}, {(location.split(';')[0])}"
        self.order_location = location
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_geo = types.KeyboardButton(text="Отправить текущее местоположение", request_location=True)
        keyboard.add(button_geo)
        self.bot.send_message(self.id, f"location: {location}", reply_markup=keyboard)


    def _route_req(self):
        url = "https://graphhopper.com/api/1/route"

        query = {
            "profile": "car",
            "point": [self.personal_location_str, self.order_location],
            "curbside": "any",
            "locale": "en",
            "elevation": "false",
            "optimize": "false",
            "instructions": "true",
            "calc_points": "true",
            "debug": "false",
            "points_encoded": "true",
            "ch.disable": "false",
            "heading": "0",
            "heading_penalty": "120",
            "pass_through": "false",
            "algorithm": "round_trip",
            "round_trip.distance": "10000",
            "round_trip.seed": "0",
            "alternative_route.max_paths": "2",
            "alternative_route.max_weight_factor": "1.4",
            "alternative_route.max_share_factor": "0.6",
            "key": "ключ"
        }

        response = requests.get(url, params=query)

        data = response.json()
        return data

# _make_request()
