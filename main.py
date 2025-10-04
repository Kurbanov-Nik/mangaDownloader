import re
import requests
import os
import json


def getUrlMangaName(url):
    pattern = re.compile(r"[0-9]+-(-[a-z]+)+", re.I)
    return url.split("?")[0][pattern.search(url).start():]

def getFirstResponse(url):
    header = {
        "Referer": "https://mangalib.me/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }
    response = requests.request("GET", url = url, headers = header)
    return response

def getAboutInfo(urlMangaName, header):
    queryParams = {
        "fields[]":
            ["background", "eng_name", "otherNames", "summary", "releaseDate", "type_id", "caution",
             "views", "close_view", "rate_avg", "rate", "genres", "tags", "teams", "user", "franchise",
             "authors", "publisher", "userRating", "moderated", "metadata", "metadata.count",
             "metadata.close_comments", "manga_status_id", "chap_count", "status_id", "artists", "format"]
    }
    url = "https://api.cdnlibs.org/api/manga/" + urlMangaName
    response = requests.request("GET", url, headers = header, params = queryParams)
    return response.json()

def getChaptersInfo(urlMangaName, header):
    url = "https://api.cdnlibs.org/api/manga/" + urlMangaName + "/chapters"
    response = requests.request("GET", url, headers = header)
    return response.json()

def collectMangaInfo(url):
    urlMangaName = getUrlMangaName(url)
    url = "https://mangalib.me/ru/manga/" + urlMangaName + "?section=info"
    response = getFirstResponse(url)
    if not response.status_code == 200:
        print("Error: %d" % response.status_code)
        return

    if not os.path.exists(urlMangaName):
        os.mkdir(urlMangaName)
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
    aboutInfo = getAboutInfo(urlMangaName, header)
    with open("%s\\aboutInfo.json" % urlMangaName, "w", encoding = 'utf-8') as file:
        json.dump(aboutInfo, file, ensure_ascii = False, indent = 4)
    chaptersInfo = getChaptersInfo(urlMangaName, header)
    with open("%s\\chaptersInfo.json" % urlMangaName, "w", encoding = 'utf-8') as file:
        json.dump(chaptersInfo, file, ensure_ascii = False, indent = 4)

def main():
    url = "https://mangalib.me/ru/manga/141625--bunsin-eulo-jadongsanyan"
    collectMangaInfo(url)

if __name__ == "__main__":
    main()