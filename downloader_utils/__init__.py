from .MangaLib.MangaLib import MangaLib
from .MangaLib.MangaLibSession import MangaLibSessions
from .UserAgentManager import UserAgentManager

SUPPORTED_SITES = {
    "mangalib.me" : (MangaLib, MangaLibSessions)
}