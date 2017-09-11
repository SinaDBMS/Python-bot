def read_tasks():
    time_hashtags = []
    with open("tasks.txt") as f:
        for line in f.readlines():
            line = line.replace(" ", "").split("-")
            time = line[0].split(":")
            hashtags = line[1].replace("[", "").replace("]", "").split(",")
            kind = line[2].strip()
            hh, mm, ss = int(time[0]), int(time[1]), int(time[2])
            time_hashtags.append(TimeHashtags(hh, mm, ss, hashtags, kind))
    return time_hashtags


class Post:
    photo = "Photo"
    galerie = "Galerie"
    video = "Video"
    audio = "Audio"
    lyrik = "Lyrik"
    voice = "Voice"

    def __init__(self, caption, file_id, kind):
        self.caption = caption
        self.file_id = file_id
        self.kind = kind


class TimeHashtags:
    def __init__(self, h, m, s, hashtags, kind):
        self.seconds = h * 3600 + m * 60 + s
        self.hashtags = hashtags
        self.kind = kind
