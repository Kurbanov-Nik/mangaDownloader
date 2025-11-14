from downloader_utils import *
import re

class ConsoleIntermediary:
    def __init__(self):
        self.manga = None
        self.session = None
        self.domain = None
        self.agent = UserAgentManager()

    def validateURL(self, url):
        pattern = re.compile(r"^https?://[A-Z0-9.-]+(?:/|/\S+)?$", re.IGNORECASE)
        if not pattern.fullmatch(url):
            print("Указанная ссылка не корректна")
            return False
        domain = self.extractURLDomain(url)
        if not domain in SUPPORTED_SITES:
            print("Сайт %s не поддерживается программой" % domain)
            return False
        self.domain = domain
        return True

    def extractURLDomain(self, url):
        return url.split("://")[1].split("/")[0]

    def setupDownloader(self):
        if self.domain:
            self.manga = SUPPORTED_SITES[self.domain][0]()
            self.session = SUPPORTED_SITES[self.domain][1]()

    def checkConnection(self):
        ...

if __name__ == "__main__":
    obj = ConsoleIntermediary()
    url = "docs-python.ru/"
    obj.checkURL(url)

    print("/".join("https://war.dog/lol/123".split("/")[0:3]))