from BranchInfo import BranchInfo
from extraFunctions import getCardinalNumeralEnding

class BranchesList:
    def __init__(self):
        self.branchesList = {}

    def addChapter(self, chapter):
        for branch in chapter["branches"]:
            branchTeams = []
            for team in branch["teams"]:
                branchTeams.append((team["id"], team["name"]))
            self.branchesList.setdefault(branch["id"], BranchInfo()).addChapter({
                "chapterIndex": chapter["index"] - 1,
                "publishDate": branch["created_at"],
                "teams": branchTeams,
                "publishUser": (branch["user"]["id"], branch["user"]["username"]),
                "restrictedView": True if branch["restricted_view"] else False})

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