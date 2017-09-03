from threading import Thread

from flask import Flask
from bot_thread import start_bot_thread
from post_scheduling import start_scheduling

application = Flask(__name__)


@application.route("/")
def hello():
    return "Hello World!"


@application.before_first_request
def initialize_bot():
    print("Starting initialization of the bot...")
    thread1 = Thread(target=start_scheduling)  # Caution start_scheduling()
    thread2 = Thread(target=start_bot_thread)  # start_scheduling()
    thread1.start()
    thread2.start()
    print("Finishing initialization of the bot...")


print("main....")
if __name__ == "__main__":
    application.run()
    print("in main")
