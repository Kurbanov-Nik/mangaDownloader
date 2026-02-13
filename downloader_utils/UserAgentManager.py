import random as rand
import re
import requests
from bs4 import BeautifulSoup

class UserAgentManager:
    defaultAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"

    def __init__(self):
        self.agentList = list()
        self.agentPattern = re.compile(r"^\w+/(?:\d+.?)+ \(.+\) \w+/(?:\d+.?)+.*$", re.I)
        self.checkAgent = True

    def toggleCheckAgent(self):
        self.checkAgent = not self.checkAgent

    def agentCheckStatus(self):
        return self.checkAgent

    def collectFromFile(self, path = "extra_files/user-agents.txt"):
        with open(path, "r") as f:
            agents = filter(lambda elem: elem.strip() and not elem in self.agentList, f.read().splitlines())
        if self.checkAgent:
            agents = filter(lambda elem: re.match(self.agentPattern, elem), agents)
        self.agentList.extend(agents)

    def collectFromWeb(self):
        response = requests.get("https://user-agents.net/", headers = {"User-Agent" : self.defaultAgent})
        webPage = BeautifulSoup(response.text, "html.parser")
        targetList = webPage.find("ul", class_ = "agents_list").find_all("a")
        trashPattern = re.compile(r"(?: \[.+]| \([^()]+\)|, [a-z]+:(?:\d+.?)+)$", re.I)
        for elem in targetList:
            if self.checkAgent and not re.match(self.agentPattern, elem.text):
                continue
            trashTail = re.search(trashPattern, elem.text)
            if trashTail:
                self.agentList.append(elem.text[0:trashTail.start()])
            else:
                self.agentList.append(elem.text)

    def addAgents(self, agents):
        agents = filter(lambda elem: not elem in self.agentList, [*agents])
        if self.checkAgent:
            agents = filter(lambda elem: re.match(self.agentPattern, elem), agents)
        self.agentList.extend(agents)

    def getAgent(self):
        if not self.agentList:
            return self.defaultAgent
        rand.shuffle(self.agentList)
        return self.agentList.pop()