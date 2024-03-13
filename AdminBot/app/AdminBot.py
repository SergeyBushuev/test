import threading

import telebot


class AdminBot:
    user_order = {}
    id: str

    def __init__(self):
        self.bot = telebot.TeleBot('ключ бота')
        self.bot.set_webhook()

        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.id = message.chat.id
            self.bot.send_message(message.chat.id, "Добро пожаловать admin bot")

    def start_bot(self):
        x = threading.Thread(name="menu", target=self.bot.polling, )
        x.start()

    def order_confirm(self, user, location, order):
        self.bot.send_message(self.id, f"location: {location}, order: {order}")
        return

    def track_courier(self, user, location, order):
        self.bot.send_message(self.id, f"location: {location}, order: {order}")
        #TODO tracking
        return

# _make_request()
