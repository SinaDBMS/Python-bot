def read_tasks():
    time_hashtags = []
    with open("tasks.txt") as f:
        for line in f.readlines():
            line = line.replace(" ", "").split("-")
            time = line[0].split(":")
            hashtags = line[1].replace("[", "").replace("]", "").split(",")
            hh, mm, ss = int(time[0]), int(time[1]), int(time[2])
            time_hashtags.append(TimeHashtags(hh, mm, ss, hashtags))
    return time_hashtags


class Post:
    photo = "Photo"
    galerie = "Galerie"
    video = "Video"
    audio = "Audio"
    lyrik = "Lyrik"
    voice = "Voice"

    def __init__(self, caption, file_id, type):
        self.caption = caption
        self.file_id = file_id
        self.type = type


class TimeHashtags:
    def __init__(self, h, m, s, hashtags):
        self.seconds = h * 3600 + m * 60 + s
        self.hashtags = hashtags
