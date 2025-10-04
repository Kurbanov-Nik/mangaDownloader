import requests
import random as rand
import re
import time

def getMangaPathName(url):
    pattern = re.compile(r"[0-9]+-(-[a-z]+)+", re.I)
    return pattern.search(url).group(0)

def getFirstResponse(url):
    header = {
        "Referer": "https://mangalib.me/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }
    response = requests.request("GET", url = url, headers = header)
    return response

def getCookiesFromResponse():
    pass

def getMangaInfo(mangaPathName):
    url = "https://mangalib.me/ru/manga/" + mangaPathName + "?section=info"
    response = getFirstResponse(url)
    info = {"available-status": False}
    if response.status_code == 200:
        info["available-status"] = True
    # getCookiesFromResponse()
    pass

def main():
    url = "https://mangalib.me/ru/manga/141625--bunsin-eulo-jadongsanyan"
    mangaPathName = getMangaPathName(url)
    getMangaInfo(mangaPathName)

if __name__ == "__main__":
    main()