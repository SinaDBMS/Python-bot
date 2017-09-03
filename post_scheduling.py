from datetime import timedelta as Timedelta, datetime as Datetime, timedelta
from sched import scheduler as Scheduler
from telegram.bot import Bot
from core_functions import *
from post_structure import Post


def task():
    now = Datetime.now()
    print("Execution of task started at: {}".format(now))
    now_in_seconds = __to_seconds(now)
    posts = load_queue()
    post = None
    lyric = None
    if abs(now_in_seconds - __H01) < 10:
        post = get_first_relevant_post(["#Galerie", "#Spruch_des_Tages"], Post.photo, posts)
    elif abs(now_in_seconds - __H08) < 10:
        post = get_first_relevant_post(["#Video"], Post.video, posts)
    elif abs(now_in_seconds - __H10) < 10:
        pass
    elif abs(now_in_seconds - __H11) < 10:
        post = get_first_relevant_post(["#Galerie", "#Geschichte"], Post.photo, posts)
    elif abs(now_in_seconds - __H13) < 10:
        post = get_first_relevant_post(["#Galerie", "#Wissen"], Post.photo, posts)
    elif abs(now_in_seconds - __H17) < 10:
        post = get_first_relevant_post(["#Video"], Post.video, posts)
    elif abs(now_in_seconds - __H20) < 10:
        post = get_first_relevant_post(["#Galerie", "#lustig"], Post.photo, posts)
    elif abs(now_in_seconds - __H21) < 10:
        pass
    elif abs(now_in_seconds - __H22) < 10:
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

        message = "{} post(s) sent to {} and removed from the queue.".format(x, get_current_channel_name())
        journal_bot.send_message(chat_id=get_masters_id(), text=message)
        print(message)


def start_scheduling():
    now = Datetime.now()
    now_in_seconds = now.minute * 60 + now.second
    print("Scheduler started at: {}".format(now))
    starting_time = 0
    if 60 <= now_in_seconds < 1860:
        starting_time = 1800 - now_in_seconds
    elif 1860 <= now_in_seconds < 3600:
        starting_time = 3600 - now_in_seconds

    i = 1
    while True:
        print("Iteration No. {}: scheduler starts in {} seconds.".format(i, starting_time))
        scheduler.enter(starting_time, 1, task)
        scheduler.run()
        starting_time = __period
        if Datetime.now().second % 10 > 2:
            starting_time -= 1
        i += 1


def __to_seconds(t):
    return t.hour * 3600 + t.minute * 60 + t.second


def __convert_to_local_time(t):
    return t - (4.5 * 3600)


####################################################################
test_bot_token = "425426086:AAFtPbcx_YNjAzZgdudQyQ5yuQ48x2g6O6A"
main_bot_token = "413427401:AAEgcTahApxJLAPGHK43TfJAl40K7CdJ8pw"
journal_bot = Bot(main_bot_token)
scheduler = Scheduler()

__period = Timedelta(minutes=30).total_seconds()
__H01 = __convert_to_local_time(1 * 3600 + 0 * 60 + 0)
__H08 = __convert_to_local_time(8 * 3600 + 30 * 60 + 0)
__H10 = __convert_to_local_time(10 * 3600 + 0 * 60 + 0)
__H11 = __convert_to_local_time(11 * 3600 + 0 * 60 + 0)
__H13 = __convert_to_local_time(13 * 3600 + 0 * 60 + 0)
__H17 = __convert_to_local_time(17 * 3600 + 0 * 60 + 0)
__H20 = __convert_to_local_time(20 * 3600 + 0 * 60 + 0)
__H21 = __convert_to_local_time(21 * 3600 + 0 * 60 + 0)
__H22 = __convert_to_local_time(22 * 3600 + 30 * 60 + 0)
