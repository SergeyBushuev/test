import asyncio
import subprocess
import requests
from flask import Flask
from flask import request

from AdminBot import AdminBot

app = Flask(__name__)
admin_bot = AdminBot()


@app.route("/")
def hello():
    return "Hello Admin!"


@app.route("/start_bot", methods=['GET', 'POST'])
def start():
    return "bot_started"


@app.route("/process_order")
def process_order():
    print(request.headers)
    user = request.headers["User"]
    location = request.headers["location"]
    order = request.headers["Order"]
    admin_bot.order_confirm(user, location, order)

    headers = {'location': location}
    requests.Request = requests.get("http://127.0.0.1:5002/process_delivery", headers=headers)

    return "order_processed"


@app.route("/courier_tracking")
def courier_tracking():
    print(request.headers)

    headers = {'location': "location"}


    return "order_processed"


if __name__ == "__main__":
    admin_bot.start_bot()
    app.run(host="0.0.0.0", port=5001)
