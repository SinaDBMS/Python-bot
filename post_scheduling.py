from datetime import timedelta as Timedelta, datetime as Datetime
from sched import scheduler as Scheduler
import pickle

from post_structure import Post

__period = Timedelta(minutes=1).total_seconds()
__times = []
__H01 = 1
__H08 = 8
__H10 = 10
__H13 = 13
__H16 = 16
__H19 = 19
__H21 = 21
__H23 = 23
__times.append(__H01)
__times.append(__H08)
__times.append(__H10)
__times.append(__H13)
__times.append(__H16)
__times.append(__H19)
__times.append(__H21)
__times.append(__H23)


def load_queue():
    posts = []
    with open("queue.pkl", "rb") as f:
        while True:
            try:
                posts.append(pickle.load(f))
            except EOFError:
                break
    return posts


def get_first_relevant_post(hashtagslist, type, posts):
    for p in posts:
        next_post = False
        if p.type == type:
            caption = p.caption.lower()
            for h in hashtagslist:
                if h.lower() not in caption:
                    next_post = True
                    break

            if not next_post:
                return p


def task1(scheduler):
    print(Datetime.now())
    if abs(Datetime.now().second - __H01) < 1:
        post = get_first_relevant_post(["#Galerie", "Spruch_des_Tages"], Post.photo, load_queue()) ##########
    elif abs(Datetime.now().second - __H08) < 1:
        print("Nothing yet")
    elif abs(Datetime.now().second - __H10) < 1:
        get_first_relevant_post(["#Video"], Post.video, load_queue())
    elif abs(Datetime.now().second - __H13) < 1:
        get_first_relevant_post(["#Galerie", "#Wissen"], Post.photo, load_queue())
    elif abs(Datetime.now().second - __H16) < 1:
        get_first_relevant_post(["#Video"], Post.video, load_queue())
    elif abs(Datetime.now().second - __H19) < 1:
        get_first_relevant_post(["#Galerie", "#Lustig"], Post.photo, load_queue())
    elif abs(Datetime.now().second - __H21) < 1:
        print("Nothing yet")
    elif abs(Datetime.now().second - __H23) < 1:
        print("Nothing yet")

    scheduler.enter(__period, 1, task1, [scheduler])


def threaded_function():
    scheduler = Scheduler()
    for tm in __times:
        starting_time = tm - Datetime.now().second
        if starting_time < 0:
            starting_time += __period

        scheduler.enter(starting_time, 1, task1, [scheduler])

    scheduler.run()
