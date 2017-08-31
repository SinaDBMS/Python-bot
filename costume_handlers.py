"""
bot --> from telegram.bot import Bot
update --> from telegram.update import Update
"""
import logging
import os
import pickle

from post_structure import Post

__das_deutsche_journal_channel = "-1001142145062"
__test_channel = "-1001104151930L"
__target_channel = __test_channel
__sina_id = 70665502


def photo_handler(bot, update):
    print("Photo_handler triggered by {}:".format(update.message.chat.username))
    try:
        caption = update.message.caption
        file_id = update.message.photo[0].file_id
        __append_to_file("queue.pkl", Post(caption, file_id, Post.photo))
        __check_sina_id(bot, update)
    except Exception:
        message = "Exception in " + __name__ + ": photo_handler"
        logging.exception(message)
        bot.send_message(chat_id=__sina_id, text=message)


def video_handler(bot, update):
    print("Video_handler triggered by {}:".format(update.message.chat.username))
    try:
        caption = update.message.caption
        file_id = update.message.video.file_id
        __append_to_file("queue.pkl", Post(caption, file_id, Post.video))
        __check_sina_id(bot, update)
    except Exception:
        message = "Exception in " + __name__ + ": video_handler"
        logging.exception(message)
        bot.send_message(chat_id=__sina_id, text=message)


def audio_handler(bot, update):
    print("Audio_handler triggered by {}:".format(update.message.chat.username))
    try:
        caption = update.message.caption
        file_id = update.message.audio.file_id
        __append_to_file("queue.pkl", Post(caption, file_id, Post.audio))
        __check_sina_id(bot, update)
    except Exception:
        message = "Exception in " + __name__ + ": audio_handler"
        logging.exception(message)
        bot.send_message(chat_id=__sina_id, text=message)


def view_queue_handler(bot, update):
    print("View_queue_handler triggered by {}:".format(update.message.chat.username))
    posts = __read_queue()
    bot.send_message(chat_id=update.message.chat_id, text="{} post(s) in the queue to be sent:".format(len(posts)))
    i = 1

    for p in posts:
        bot.send_message(chat_id=update.message.chat_id, text="Post{}".format(i))
        i += 1

        if p.type == Post.photo:
            bot.send_photo(caption=p.caption, chat_id=update.message.chat_id, photo=p.file_id)
        elif p.type == Post.video:
            bot.send_video(caption=p.caption, chat_id=update.message.chat_id, video=p.file_id)
        elif p.type == Post.audio:
            bot.send_audio(caption=p.caption, chat_id=update.message.chat_id, audio=p.file_id)


def empty_queue_handler(bot, update):
    print("Empty_queue_handler triggered by {}:".format(update.message.chat.username))
    with open("queue.pkl", "w"):
        pass

    bot.send_message(chat_id=update.message.chat_id, text="Successfully cleared all posts in the queue.")


def delete_post_handler(bot, update, args):
    print("Delete_post_handler triggered by {}:".format(update.message.chat.username))
    posts = __read_queue()
    junks = []
    initial_size = len(posts)

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

    for j in junks:
        posts.remove(j)

    if initial_size != len(posts):
        __write_to_file("queue.pkl", posts)
        bot.send_message(chat_id=update.message.chat_id, text="Successfully removed post(s).")


def manual_send_handler(bot, update, args):
    print("Manual_send_handler triggered by {}:".format(update.message.chat.username))
    posts = __read_queue()
    junks = []
    initial_size = len(posts)

    for a in args:
        try:
            p = posts[int(a) - 1]
            if p.type == Post.photo:
                bot.send_photo(caption=p.caption, chat_id=__target_channel, photo=p.file_id)
            elif p.type == Post.video:
                bot.send_video(caption=p.caption, chat_id=__target_channel, video=p.file_id)
            elif p.type == Post.audio:
                bot.send_audio(caption=p.caption, chat_id=__target_channel, audio=p.file_id)
            junks.append(p)
        except ValueError:
            message = "Invalid argument: {}. Required a number.".format(a)
            print(message)
            bot.send_message(chat_id=update.message.chat_id, text=message)
        except IndexError:
            message = "Maximum Number allowed: {}. {} given.".format(len(posts), a)
            print(message)
            bot.send_message(chat_id=update.message.chat_id, text=message)

    for j in junks:
        posts.remove(j)

    if initial_size != len(posts):
        __write_to_file("queue.pkl", posts)
        bot.send_message(chat_id=update.message.chat_id, text="Successfully sent post(s).")


def change_target_channel(bot, update):
    global __target_channel

    if __target_channel == __test_channel:
        __target_channel = __das_deutsche_journal_channel

    elif __target_channel == __das_deutsche_journal_channel:
        __target_channel = __test_channel
        print("test")

    if __target_channel == __das_deutsche_journal_channel:
        message = "Das deutsche Journal"
    elif __target_channel == __test_channel:
        message = "Test Channel"

    message = "Successfully switched to {}: {}.".format(message, __target_channel)
    print(message)
    bot.send_message(chat_id=update.message.chat_id, text=message)


def view_target_channel(bot, update):
    channel = "Test Channel"
    if __target_channel == __das_deutsche_journal_channel:
        channel = "Das deutsche Journal"
    elif __target_channel == __test_channel:
        channel = "Test Channel"

    message = "Target channel set to {}: {}.".format(channel, __target_channel)
    print(message)
    bot.send_message(chat_id=update.message.chat_id, text=message)


def get_queue_handler(bot, update):
    print("get_queue_handler triggered by {}:".format(update.message.chat.username))
    if os.path.getsize("queue.pkl") > 0:
        bot.send_document(chat_id=update.message.chat_id, document=open("queue.pkl", 'rb'))
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Empty file.")


def __write_to_file(file_name, posts_list):
    with open(file_name, "wb") as f:
        for p in posts_list:
            pickle.dump(p, f)


def __append_to_file(file_name, post):
    with open(file_name, "ab") as f:
        pickle.dump(post, f)


def __check_sina_id(bot, update):
    global __sina_id
    if update.message.chat.username == "Sina_bd":
        __sina_id = update.message.chat.id
        print("This is the current id of Sina_bd: {}".format(__sina_id))


def __read_queue():
    posts = []
    with open("queue.pkl", "rb") as f:
        while True:
            try:
                posts.append(pickle.load(f))
            except EOFError:
                break
    return posts
