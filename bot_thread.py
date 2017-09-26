from telegram.ext.commandhandler import CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.updater import Updater
from costume_handlers import *

test_bot_token = "425426086:AAFtPbcx_YNjAzZgdudQyQ5yuQ48x2g6O6A"
main_bot_token = "413427401:AAEgcTahApxJLAPGHK43TfJAl40K7CdJ8pw"


def start_bot_thread():
    print("Start bot Thread started...")
    updater = Updater(main_bot_token)
    dispatcher = updater.dispatcher
    # logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    photo = MessageHandler(Filters.photo, photo_handler)
    video = MessageHandler(Filters.video, video_handler)
    audio = MessageHandler(Filters.audio, audio_handler)
    voice = MessageHandler(Filters.voice, voice_handler)
    document = MessageHandler(Filters.document, document_handler)
    view_q = CommandHandler('viewqueue', view_queue_handler)
    view_c = CommandHandler('viewchannel', view_target_channel)
    change_c = CommandHandler('changechannel', change_target_channel)
    empty_q = CommandHandler('emptyqueue', empty_queue_handler)
    delete_p = CommandHandler('deletepost', delete_post_handler, pass_args=True)
    send_p = CommandHandler('sendpost', manual_send_handler, pass_args=True)
    get_q = CommandHandler('getqueue', get_queue_handler)
    get_t = CommandHandler('gettasks', get_tasks_handler)
    get_t_z_d = CommandHandler('gettimediff', get_time_zone_diff_handler)
    set_t_z_d = CommandHandler('settimediff', set_time_zone_diff_handler, pass_args=True)

    dispatcher.add_handler(photo)
    dispatcher.add_handler(video)
    dispatcher.add_handler(audio)
    dispatcher.add_handler(voice)
    dispatcher.add_handler(document)
    dispatcher.add_handler(view_q)
    dispatcher.add_handler(view_c)
    dispatcher.add_handler(change_c)
    dispatcher.add_handler(empty_q)
    dispatcher.add_handler(delete_p)
    dispatcher.add_handler(send_p)
    dispatcher.add_handler(get_q)
    dispatcher.add_handler(get_t)
    dispatcher.add_handler(get_t_z_d)
    dispatcher.add_handler(set_t_z_d)
    updater.start_polling()
    print("Ending initialization of the bot...")
