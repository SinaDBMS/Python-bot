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
    print("Photo_handler:")
    try:
        caption = update.message.caption
        file_id = update.message.photo[0].file_id
        __append_to_file("queue.pkl", Post(caption, file_id, Post.photo))
        __check_sina_id(bot, update)
    except Exception:
        message = "Exception in " + __name__ + ": photo_handler"
        logging.exception(message)
        bot.send_message(chat_id=sina_id, text=message)


def video_handler(bot, update):
    print("Video_handler")
    try:
        caption = update.message.caption
        file_id = update.message.video.file_id
        __append_to_file("queue.pkl", Post(caption, file_id, Post.video))
        __check_sina_id(bot, update)
    except Exception:
        message = "Exception in " + __name__ + ": video_handler"
        logging.exception(message)
        bot.send_message(chat_id=sina_id, text=message)


def view_queue_handler(bot, update):
    print("View_queue:")
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


def empty_queue_handler(bot, update):
    print("Empty_queue:")
    with open("queue.pkl", "w"):
        pass

    bot.send_message(chat_id=update.message.chat_id, text="Successfully cleared all posts in the queue.")


def delete_post(bot, update, args):
    posts = __read_queue()
    initial_size = len(posts)

    for a in args:
        try:
            del posts[int(a) - 1]
        except ValueError:
            message = "Invalid argument: {}. Required a number.".format(a)
            print(message)
            bot.send_message(chat_id=update.message.chat_id, text=message)
        except IndexError:
            message = "Maximum Number allowed: {}".format(len(posts))
            print(message)
            bot.send_message(chat_id=update.message.chat_id, text=message)

    if initial_size != len(posts):
        __write_to_file("queue.pkl", posts)
        bot.send_message(chat_id=update.message.chat_id, text="Successfully removed post(s).")


def __write_to_file(file_name, posts_list):
    with open(file_name, "wb") as f:
        for p in posts_list:
            pickle.dump(p, f)


def __append_to_file(file_name, post):
    with open(file_name, "ab") as f:
        pickle.dump(post, f)


def __check_sina_id(bot, update):
    if update.message.chat.username == "Sina_bd":
        sina_id = update.message.chat.id
        print("This is the current id of Sina_bd: {}".format(sina_id))


def __read_queue():
    posts = []
    with open("queue.pkl", "rb") as f:
        while True:
            try:
                posts.append(pickle.load(f))
            except EOFError:
                break
    return posts
