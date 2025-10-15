from ChaptersList import ChaptersList
from BranchesList import BranchesList

class MangaInfo:
    def __init__(self, manga):
        self.id = manga["id"]
        self.name = manga["name"]
        self.ageRestriction = manga["ageRestriction"]
        self.type = manga["type"]
        self.closeView = manga["closeView"]
        self.releaseDate = manga["releaseDate"]
        self.status = manga["status"]
        self.scanlateStatus = manga["scanlateStatus"]
        self.branches = BranchesList()
        self.chapters = ChaptersList()

    def addChapter(self, chapter):
        self.branches.addChapter(chapter)
        self.chapters.addChapter(chapter)

    def __str__(self):
        resStr = "%s: %s (%s)\nДата релиза: %s\nСтатус: %s\nСтатус перевода: %s" % (
            self.type[1],
            self.name,
            self.ageRestriction[1],
            self.releaseDate,
            self.status[1],
            self.scanlateStatus[1])
        return resStr