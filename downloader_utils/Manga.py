from abc import ABC, abstractmethod

class Manga(ABC):
    def __init__(self):
        self.name = None
        self.chapterAmount = 0
        self.extraChapterAmount = 0
        self.chapterList = []
        self.extraChapterList = []
        self.hasBranches = False
    ...