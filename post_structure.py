class Post:
    photo = "Photo"
    galerie = "Galerie"
    video = "Video"
    audio = "Audio"
    lyrik = "Lyrik"

    def __init__(self, caption, file_id, type):
        self.caption = caption
        self.file_id = file_id
        self.type = type
