import pickle

from data_structures import Post

__das_deutsche_journal_channel = "-1001142145062"
__test_channel = "-1001104151930L"
__target_channel = __test_channel
__sina_id = 70665502
__time_zone_diff = 4.5


def delete_posts(junks, posts):  # change the name
    initial_size = len(posts)
    for j in junks:
        posts.remove(j)

    if initial_size != len(posts):
        __write_to_file("queue.pkl", posts)

    return initial_size - len(posts)


def send_post(bot, target, post):
    if post.kind == Post.photo:
        bot.send_photo(caption=post.caption, chat_id=target, photo=post.file_id)
    elif post.kind == Post.video:
        bot.send_video(caption=post.caption, chat_id=target, video=post.file_id)
    elif post.kind == Post.audio:
        bot.send_audio(caption=post.caption, chat_id=target, audio=post.file_id)
    elif post.kind == Post.voice:
        bot.send_voice(caption=post.caption, chat_id=target, voice=post.file_id)


def get_first_relevant_post(hashtagslist, kind, posts):
    for p in posts:
        next_post = False
        if p.kind == kind:
            caption = p.caption
            if caption is None:
                caption = ""
            caption = caption.lower()

            for h in hashtagslist:
                if h.lower() not in caption:
                    next_post = True
                    break

            if not next_post:
                return p


def change_current_channel():
    global __target_channel
    if __target_channel == __test_channel:
        __target_channel = __das_deutsche_journal_channel
    elif __target_channel == __das_deutsche_journal_channel:
        __target_channel = __test_channel
    return __target_channel


def get_current_channel_id():
    return __target_channel


def get_current_channel_name():
    if __target_channel == __das_deutsche_journal_channel:
        return "Das deutsche Journal"
    elif __target_channel == __test_channel:
        return "Test Channel"


def load_queue():
    posts = []
    with open("queue.pkl", "rb") as f:
        while True:
            try:
                posts.append(pickle.load(f))
            except EOFError:
                break
    return posts


def get_masters_id():
    return __sina_id


def set_masters_id(new_id):
    global __sina_id
    __sina_id = new_id


def check_sina_id(update):
    if update.message.chat.username == "Sina_bd":
        if update.message.chat.id != get_masters_id():
            set_masters_id(update.message.chat.id)


def set_time_zone_diff(t):
    global __time_zone_diff
    __time_zone_diff = t


def get_time_zone_diff():
    return __time_zone_diff


def __write_to_file(file_name, posts_list):
    with open(file_name, "wb") as f:
        for p in posts_list:
            pickle.dump(p, f)


def append_to_file(file_name, post):
    with open(file_name, "ab") as f:
        pickle.dump(post, f)
