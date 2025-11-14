from ..RequestSession import RequestSession
import requests

class MangaLibSessions(RequestSession):
    def __init__(self, agent):
        super().__init__(agent)
        self.__mainPage = "https://mangalib.me/ru"
        self.session = None

    @property
    def mainPage(self):
        return self.__mainPage

    @mainPage.setter
    def mainPage(self, val):
        self.__mainPage = val

    def collectMangaInfo(self):
        ...

    def collectChapters(self):
        ...