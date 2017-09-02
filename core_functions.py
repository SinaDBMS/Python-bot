import pickle

from post_structure import Post

__das_deutsche_journal_channel = "-1001142145062"
__test_channel = "-1001104151930L"
__target_channel = __test_channel


def delete_posts(junks, posts): #change the name
    initial_size = len(posts)
    for j in junks:
        posts.remove(j)

    if initial_size != len(posts):
        __write_to_file("queue.pkl", posts)

    return initial_size - len(posts)


def send_post(bot, target, post):
    if post.type == Post.photo:
        bot.send_photo(caption=post.caption, chat_id=target, photo=post.file_id)
    elif post.type == Post.video:
        bot.send_video(caption=post.caption, chat_id=target, video=post.file_id)
    elif post.type == Post.audio:
        bot.send_audio(caption=post.caption, chat_id=target, audio=post.file_id)


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


def __write_to_file(file_name, posts_list):
    with open(file_name, "wb") as f:
        for p in posts_list:
            pickle.dump(p, f)
