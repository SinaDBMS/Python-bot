from threading import Thread

from flask import Flask
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.updater import Updater

import costume_handlers
from costume_handlers import photo_handler, video_handler
from post_scheduling import threaded_function

application = Flask(__name__)

thread = Thread(target=threaded_function)
thread.start()


@application.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    application.run()
