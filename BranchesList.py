import BranchInfo
from extraFunctions import getCardinalNumeralEnding

class BranchesList:
    def __init__(self):
        self.branchesList = {} # branch_id, class BranchInfo

    def addChapter(self, chapter):
        for branch in chapter["branches"]:
            self.branchesList.setdefault(branch["id"], BranchInfo()).addChapter(chapter)

    def getBranchesAmount(self):
        return len(self.branchesList)

    def __str__(self):
        firstStr = ["ветка", "ветки", "веток"]
        resStr = "Всего %d %s" % (
            self.getBranchesAmount(),
            firstStr[getCardinalNumeralEnding(self.getBranchesAmount())])
        for i, key in enumerate(self.branchesList):
            resStr += "\nВетка # %d\n%s" % (i + 1, str(self.branchesList[key]))
        return resStr