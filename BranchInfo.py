class BranchInfo:
    def __init__(self):
        self.chapters = []
        self.teams = {}
        self.users = {}

    def addChapter(self, chapter):
        teamsId = []
        for team in chapter["teams"]:
            self.teams[team[0]] = team[1]
            teamsId.append(team[0])
        self.users[chapter["publishUser"][0]] = chapter["publishUser"][1]
        self.chapters.append((
            chapter["chapterIndex"],
            chapter["publishDate"].split("T")[0],
            teamsId,
            chapter["publishUser"][0],
            chapter["restrictedView"]))