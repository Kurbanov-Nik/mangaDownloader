import random as rand
import requests

class UserAgent:
    def __init__(self):
        self.agentList = {
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
        }

    def collectFromFile(self, path = "extra_files/user-agents.txt"):
        with open(path, "r") as f:
            data = filter(lambda x: x.strip(), f.read().splitlines())
            self.agentList.update(data)

    def collectFromWeb(self, url = None):
        ...

    def getAgent(self):
        return rand.choice(list(self.agentList))

if __name__ == "__main__":
    obj = UserAgent()
    obj.collectFromFile()