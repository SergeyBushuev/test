import asyncio
import subprocess

from flask import Flask

from MenuBot import MenuBot

app = Flask(__name__)
menu_bot = MenuBot()

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/start_bot", methods=['GET', 'POST'])
def start():
    menu_bot.start_bot()
    return "bot_started"


if __name__ == "__main__":
    menu_bot.start_bot()
    app.run()
