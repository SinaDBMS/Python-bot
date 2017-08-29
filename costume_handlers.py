"""
bot --> from telegram.bot import Bot
update --> from telegram.update import Update
"""
import logging
import pickle

from post_structure import Post

__test_channel = "-1001104151930L"
__target_channel = __test_channel
sina_id = 70665502


def photo_handler(bot, update):
    try:
        caption = update.message.caption
        file_id = update.message.photo[0].file_id
        __write_to_file("queue.pkl", Post(caption, file_id, Post.photo))
        __check_sina_id(bot, update)
    except Exception:
        message = "Exception in " + __name__ + ": photo_handler"
        logging.exception(message)
        bot.send_message(chat_id=sina_id, text=message)


def video_handler(bot, update):
    try:
        caption = update.message.caption
        file_id = update.message.video.file_id
        __write_to_file("queue.pkl", Post(caption, file_id, Post.video))
        __check_sina_id(bot, update)
    except Exception:
        message = "Exception in " + __name__ + ": video_handler"
        logging.exception(message)
        bot.send_message(chat_id=sina_id, text=message)


def view_queue(bot, update):
    posts = []
    with open("queue.pkl", "rb") as f:
        while True:
            try:
                posts.append(pickle.load(f))
            except EOFError:
                break

    bot.send_message(chat_id=sina_id, text="Here's {} posts to be sent:".format(len(posts)))
    for p in posts:
        if p.type == Post.photo:
            bot.send_photo(caption=p.caption, chat_id=update.message.chat_id, photo=p.file_id)
        elif p.type == Post.video:
            bot.send_video(caption=p.caption, chat_id=update.message.chat_id, video=p.file_id)


def __write_to_file(file_name, obj):
    with open(file_name, "ab") as f:
        pickle.dump(obj, f)


def __check_sina_id(bot, update):
    if update.message.chat.username == "Sina_bd":
        sina_id = update.message.chat.id
        print(sina_id)
