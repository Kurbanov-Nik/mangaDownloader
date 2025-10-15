from extraFunctions import getCardinalNumeralEnding

class ChaptersList:
    def __init__(self):
        self.chaptersAmount = 0
        self.extrasAmount = 0
        self.volumesAmount = 0
        self.chaptersList = []

    def addChapter(self, chapter):
        self.chaptersList.append(
            [chapter["id"],
            chapter["volume"],
            chapter["number"],
            chapter["name"]])
        self.chaptersAmount += 1
        if "." in chapter["num"]:
            self.extrasAmount += 1
        if str(self.volumesAmount) != chapter["vol"]:
            self.volumesAmount += 1

    def getChapter(self, index = 0):
        return self.chaptersList[index]

    def __str__(self):
        firstStr = ["глава", "главы", "глав"]
        secondStr = " (из которых %d экстра)" if self.extrasAmount > 0 else ""
        thirdStr = ["томе", "томах", "томах"]
        return "Всего %d %s%s в %d %s" % (
            self.chaptersAmount,
            firstStr[getCardinalNumeralEnding(self.chaptersAmount)],
            secondStr,
            self.volumesAmount,
            thirdStr[getCardinalNumeralEnding(self.volumesAmount)])