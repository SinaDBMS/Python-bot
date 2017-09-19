from datetime import timedelta as Timedelta, datetime as Datetime, timedelta
from sched import scheduler as Scheduler
from telegram.bot import Bot
from core_functions import *
from data_structures import Post, read_tasks


def task():
    try:
        now = Datetime.now()
        programs = read_tasks()
        print("Execution of task started at: {}".format(now))
        now_in_seconds = __to_seconds(now)
        posts = load_queue()
        post = None
        lyric = None

        for p in programs:
            if abs(now_in_seconds - __convert_to_local_time(p.seconds)) < 10:
                if p.kind == Post.audio:
                    post = get_first_relevant_post([], Post.audio, posts)
                    lyric = get_first_relevant_post(["#Lyrik"], Post.photo, posts)
                else:
                    post = get_first_relevant_post(p.hashtags, p.kind, posts)
            if post is not None:
                break

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
    except Exception:
        print("Odd Exception Occurred...")


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
