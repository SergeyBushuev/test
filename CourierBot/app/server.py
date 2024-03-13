import asyncio
import subprocess
import requests
from flask import Flask
from flask import request


from CourierBot import CourierBot

app = Flask(__name__)
CourierBot = CourierBot()


@app.route("/")
def hello():
    return "Hello Admin!"


@app.route("/start_bot", methods=['GET', 'POST'])
def start():
    return "bot_started"


@app.route("/process_delivery")
def process_order():
    print(request.headers)
    location = request.headers["location"]
    CourierBot.delivery_confirm(location)
    return "delivery_accepted"



if __name__ == "__main__":
    CourierBot.start_bot()
    app.run(host="0.0.0.0", port=5002)
