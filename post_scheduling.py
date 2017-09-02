from datetime import timedelta as Timedelta, datetime as Datetime, timedelta
from sched import scheduler as Scheduler
import time
from telegram.bot import Bot
from core_functions import *
from post_structure import Post


def task1(scheduler):
    now = Datetime.now()
    now_in_seconds = __to_seconds(now)
    print(now)
    posts = load_queue()
    post = None
    lyric = None
    if abs(now_in_seconds - __H01) < 1:
        post = get_first_relevant_post(["#Galerie", "#Spruch_des_Tages"], Post.photo, posts)
    elif abs(now_in_seconds - __H08) < 1:
        post = get_first_relevant_post(["#Video"], Post.video, posts)
    elif abs(now_in_seconds - __H10) < 1:
        pass
    elif abs(now_in_seconds - __H13) < 1:
        post = get_first_relevant_post(["#Galerie", "#Wissen"], Post.photo, posts)
    elif abs(now_in_seconds - __H17) < 1:
        post = get_first_relevant_post(["#Video"], Post.video, posts)
    elif abs(now_in_seconds - __H19) < 1:
        post = get_first_relevant_post(["#Galerie", "#lustig"], Post.photo, posts)
    elif abs(now_in_seconds - __H21) < 1:
        pass
    elif abs(now_in_seconds - __H22) < 1:
        post = get_first_relevant_post([], Post.audio, posts)
        lyric = get_first_relevant_post(["#Lyrik"], Post.photo, posts)

    if post is not None:
        if lyric is not None:
            send_post(journal_bot, get_current_channel_id(), post)
            send_post(journal_bot, get_current_channel_id(), lyric)
            x = delete_posts([post, lyric], posts)
        else:
            send_post(journal_bot, get_current_channel_id(), post)
            x = delete_posts([post], posts)

        journal_bot.send_message(chat_id="70665502", text="{} post(s) sent to {} and removed from the "
                                                          "queue.".format(x, get_current_channel_id()))

    scheduler.enter(__period, 1, task1, [scheduler])


def get_tasks_queue(bot, update):
    for t in scheduler.queue:
        print(t.time)
        bot.send_message(chat_id=update.message.chat_id, text=t.time)


def start_scheduling():
    for tm in __times:
        now = Datetime.now()
        starting_time = tm - __to_seconds(now)
        if starting_time < 0:
            starting_time += __period

        scheduler.enter(starting_time, 1, task1, [scheduler])

    scheduler.run()


def __to_seconds(t):
    return t.hour * 3600 + t.minute * 60 + t.second


def __convert_to_local_time(t):
    return t + (-12600 - time.timezone)


####################################################################
journal_bot = Bot('425426086:AAFtPbcx_YNjAzZgdudQyQ5yuQ48x2g6O6A')
scheduler = Scheduler()

__period = Timedelta(days=1).total_seconds()
__times = []
__H01 = __convert_to_local_time(1 * 3600 + 0 * 60 + 0)
__H08 = __convert_to_local_time(8 * 3600 + 0 * 60 + 0)
__H10 = __convert_to_local_time(10 * 3600 + 0 * 60 + 0)
__H13 = __convert_to_local_time(13 * 3600 + 0 * 60 + 0)
__H17 = __convert_to_local_time(17 * 3600 + 0 * 60 + 0)
__H19 = __convert_to_local_time(19 * 3600 + 0 * 60 + 0)
__H21 = __convert_to_local_time(21 * 3600 + 0 * 60 + 0)
__H22 = __convert_to_local_time(22 * 3600 + 0 * 60 + 0)
__times.append(__H01)
__times.append(__H08)
__times.append(__H10)
__times.append(__H13)
__times.append(__H17)
__times.append(__H19)
__times.append(__H21)
__times.append(__H22)
