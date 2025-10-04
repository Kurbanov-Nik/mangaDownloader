import requests
import json
import random as rand
import re
import time

def getMangaPathName(url):
    pattern = re.compile(r"[0-9]+-(-[a-z]+)+", re.I)
    return url.split("?")[0][pattern.search(url).start():]

def getFirstResponse(url):
    header = {
        "Referer": "https://mangalib.me/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }
    response = requests.request("GET", url = url, headers = header)
    return response

def getCookiesFromResponse():
    pass

def getMangaInfo(mangaPathName, header):
    url = "https://mangalib.me/ru/manga/" + mangaPathName + "?section=info"
    response = getFirstResponse(url)
    # getCookiesFromResponse()
    info = {"available-status": False}

    if response.status_code == 200:
        info["available-status"] = True
    else:
        return info

    querystring = {
        "fields[]": ["background", "eng_name", "otherNames", "summary", "releaseDate", "type_id", "caution",
                         "views", "close_view", "rate_avg", "rate", "genres", "tags", "teams", "user", "franchise",
                         "authors", "publisher", "userRating", "moderated", "metadata", "metadata.count",
                         "metadata.close_comments", "manga_status_id", "chap_count", "status_id", "artists",
                         "format"]
    }
    url = "https://api.cdnlibs.org/api/manga/" + mangaPathName
    response = requests.request("GET", url, headers = header, params = querystring)
    info.update(response.json()['data'])
    return info

def getMangaChapterInfo(mangaPathName, header):
    url = "https://api.cdnlibs.org/api/manga/" + mangaPathName + "/chapters"
    response = requests.request("GET", url, headers = header)
    return response.json()['data']

def main():
    url = "https://mangalib.me/ru/manga/141625--bunsin-eulo-jadongsanyan"
    header = {
        "Client-Time-Zone": "Europe/Moscow",
        "Content-Type": "application/json",
        "Referer": "https://mangalib.me/",
        'sec-ch-ua': "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Google Chrome\";v=\"140\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'Site-Id': "1",  # important field
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }
    mangaPathName = getMangaPathName(url)
    mangaInfo = getMangaInfo(mangaPathName, header)
    if not mangaInfo['available-status']:
        print("Указанной страницы не существует!")
        return
    mangaOrigName = mangaInfo['name']
    mangaRusName = mangaInfo['rus_name']
    chaptersInfo = getMangaChapterInfo(mangaPathName, header)

if __name__ == "__main__":
    main()