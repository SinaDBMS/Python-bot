"""
bot --> from telegram.bot import Bot
update --> from telegram.update import Update
"""
import logging
import os
from datetime import datetime

from core_functions import *
from data_structures import Post


def photo_handler(bot, update):
    print("Photo_handler triggered by {}:".format(update.message.chat.username))
    try:
        caption = update.message.caption
        file_id = update.message.photo[0].file_id
        append_to_file("queue.pkl", Post(caption, file_id, Post.photo))
        check_sina_id(update)
    except Exception:
        message = "Exception in " + __name__ + ": photo_handler"
        logging.exception(message)
        bot.send_message(chat_id=get_masters_id(), text=message)


def video_handler(bot, update):
    print("Video_handler triggered by {}:".format(update.message.chat.username))
    try:
        caption = update.message.caption
        file_id = update.message.video.file_id
        append_to_file("queue.pkl", Post(caption, file_id, Post.video))
        check_sina_id(update)
    except Exception:
        message = "Exception in " + __name__ + ": video_handler"
        logging.exception(message)
        bot.send_message(chat_id=get_masters_id(), text=message)


def audio_handler(bot, update):
    print("Audio_handler triggered by {}:".format(update.message.chat.username))
    try:
        caption = update.message.caption
        file_id = update.message.audio.file_id
        append_to_file("queue.pkl", Post(caption, file_id, Post.audio))
        check_sina_id(update)
    except Exception:
        message = "Exception in " + __name__ + ": audio_handler"
        logging.exception(message)
        bot.send_message(chat_id=get_masters_id(), text=message)


def voice_handler(bot, update):
    print("Voice_handler triggered by {}:".format(update.message.chat.username))
    try:
        caption = update.message.caption
        file_id = update.message.voice.file_id
        append_to_file("queue.pkl", Post(caption, file_id, Post.voice))
        check_sina_id(update)
    except Exception:
        message = "Exception in " + __name__ + ": voice_handler"
        logging.exception(message)
        bot.send_message(chat_id=get_masters_id(), text=message)


def document_handler(bot, update):
    print("Document_handler triggered by {}:".format(update.message.chat.username))
    try:
        with open("tasks.txt", "w") as f:
            file_id = update.message.document.file_id
            new_file = bot.get_file(file_id)
            new_file.download("tasks.txt")
        check_sina_id(update)
    except Exception:
        message = "Exception in " + __name__ + ": audio_handler"
        logging.exception(message)
        bot.send_message(chat_id=get_masters_id(), text=message)


def view_queue_handler(bot, update):
    print("View_queue_handler triggered by {}:".format(update.message.chat.username))
    posts = load_queue()
    bot.send_message(chat_id=update.message.chat_id, text="{} post(s) in the queue to be sent:".format(len(posts)))
    i = 1

    for p in posts:
        bot.send_message(chat_id=update.message.chat_id, text="Post{}".format(i))
        i += 1
        send_post(bot, update.message.chat_id, p)


def empty_queue_handler(bot, update):
    print("Empty_queue_handler triggered by {}:".format(update.message.chat.username))
    with open("queue.pkl", "w"):
        pass
    bot.send_message(chat_id=update.message.chat_id, text="Successfully cleared all posts in the queue.")


def delete_post_handler(bot, update, args):
    print("Delete_post_handler triggered by {}:".format(update.message.chat.username))
    posts = load_queue()
    junks = []

    for a in args:
        try:
            junks.append(posts[int(a) - 1])
        except ValueError:
            message = "Invalid argument: {}. Required a number.".format(a)
            print(message)
            bot.send_message(chat_id=update.message.chat_id, text=message)
        except IndexError:
            message = "Maximum Number allowed: {}. {} given.".format(len(posts), a)
            print(message)
            bot.send_message(chat_id=update.message.chat_id, text=message)

    x = delete_posts(junks, posts)
    bot.send_message(chat_id=update.message.chat_id, text="{} post(s) deleted.".format(x))


def manual_send_handler(bot, update, args):
    print("Manual_send_handler triggered by {}:".format(update.message.chat.username))
    posts = load_queue()
    junks = []

    for a in args:
        try:
            p = posts[int(a) - 1]
            send_post(bot, get_current_channel_id(), p)
            junks.append(p)
        except ValueError:
            message = "Invalid argument: {}. Required a number.".format(a)
            print(message)
            bot.send_message(chat_id=update.message.chat_id, text=message)
        except IndexError:
            message = "Maximum Number allowed: {}. {} given.".format(len(posts), a)
            print(message)
            bot.send_message(chat_id=update.message.chat_id, text=message)

    x = delete_posts(junks, posts)
    bot.send_message(chat_id=update.message.chat_id,
                     text="{} post(s) sent to {} and removed from the queue.".format(x, get_current_channel_name()))


def change_target_channel(bot, update):
    print("Change_target_channel triggered by {}:".format(update.message.chat.username))
    print(datetime.now())
    current_channel_id = change_current_channel()
    current_channel_name = get_current_channel_name()
    message = "Successfully switched to {}: {}.".format(current_channel_name, current_channel_id)
    print(message)
    bot.send_message(chat_id=update.message.chat_id, text=message)


def view_target_channel(bot, update):
    print("View_target_channel triggered by {}:".format(update.message.chat.username))
    print(datetime.now())
    message = "Current channel is {}: {}.".format(get_current_channel_name(), get_current_channel_id())
    print(message)
    bot.send_message(chat_id=update.message.chat_id, text=message)


def get_queue_handler(bot, update):
    print("get_queue_handler triggered by {}:".format(update.message.chat.username))
    if os.path.getsize("queue.pkl") > 0:
        bot.send_document(chat_id=update.message.chat_id, document=open("queue.pkl", 'rb'))
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Empty file.")


def get_tasks_handler(bot, update):
    print("Get_tasks_handler triggered by {}:".format(update.message.chat.username))
    if os.path.getsize("tasks.txt") > 0:
        bot.send_document(chat_id=update.message.chat_id, document=open("tasks.txt", 'rb'))
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Empty file.")


def set_time_zone_diff_handler(bot, update, args):
    print("Set_time_zone_diff_handler triggered by {}:".format(update.message.chat.username))
    set_time_zone_diff(float(args[0]))
    bot.send_message(chat_id=update.message.chat_id, text="New Time Zone Difference: {}".format(get_time_zone_diff()))


def get_time_zone_diff_handler(bot, update):
    print("Get_time_zone_diff_handler triggered by {}:".format(update.message.chat.username))
    bot.send_message(chat_id=update.message.chat_id, text="Time Zone Difference: {}".format(get_time_zone_diff()))
