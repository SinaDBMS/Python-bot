from telegram.ext.commandhandler import CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.updater import Updater
import costume_handlers
from costume_handlers import photo_handler, video_handler


def start_bot_thread():
    updater = Updater('413427401:AAEgcTahApxJLAPGHK43TfJAl40K7CdJ8pw')
    dispatcher = updater.dispatcher
    # logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    photo = MessageHandler(Filters.photo, photo_handler)
    video = MessageHandler(Filters.video, video_handler)
    view_q = CommandHandler('viewqueue', costume_handlers.view_queue)
    dispatcher.add_handler(photo)
    dispatcher.add_handler(video)
    dispatcher.add_handler(view_q)
    updater.start_polling()
    updater.idle()
