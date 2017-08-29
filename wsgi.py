from flask import Flask
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.updater import Updater

import costume_handlers
from costume_handlers import photo_handler, video_handler

application = Flask(__name__)


@application.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    application.run()
