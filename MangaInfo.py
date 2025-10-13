import ChaptersList

class MangaInfo:
    def __init__(self, **kwargs):
        self.id: int = kwargs["id"]
        self.name: str = kwargs["name"]
        self.ageRestriction: tuple = kwargs["ageRestriction"]
        self.type: tuple = kwargs["type"]
        self.closeView: bool = kwargs["closeView"]
        self.releaseDate: str = kwargs["releaseDate"]
        self.status: tuple = kwargs["status"]
        self.scanlateStatus: tuple = kwargs["scanlateStatus"]
        self.branches = []
        self.chapters = ChaptersList()

    def addChapter(self):
        pass

    def __str__(self):
        self.chapters = 1
        pass