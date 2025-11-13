import random as rand
import requests

class UserAgent:
    def __init__(self):
        self.defaultAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
        self.agentList = list()

    def collectFromFile(self, path = "extra_files/user-agents.txt"):
        with open(path, "r") as f:
            data = filter(lambda line: line.strip() and not line in self.agentList, f.read().splitlines())
        self.agentList.extend(data)

    def collectFromWeb(self, url = None):
        ...

    def getAgent(self):
        if not self.agentList:
            return self.defaultAgent
        rand.shuffle(self.agentList)
        return self.agentList.pop()