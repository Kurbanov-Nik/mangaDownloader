from downloader_utils import *
import re

class ConsoleIntermediary:
    def checkURL(self, url):
        pattern = re.compile(r"^https?://[A-Z0-9.-]+(?:/|/\S+)?$", re.IGNORECASE)
        if not pattern.fullmatch(url):
            print("Указанная ссылка не корректна")
            return False
        domain = self.extractURLDomain(url)
        if not domain in SUPPORTED_SITES:
            print("Сайт %s не поддерживается программой" % domain)
            return False
        return True

    def extractURLDomain(self, url):
        return url.split("://")[1].split("/")[0]