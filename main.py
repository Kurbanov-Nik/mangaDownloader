import re
import requests
import os
import json
import time
import random as rand


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
    # Age Restriction Titles (18+) can not download, because need authorization
    if aboutInfo["data"]["ageRestriction"]["id"] == 4:
        print("Ограничение 18+ : необходима авторизация на сайте")
        return
    # header["Authorization"] = "token"
    chaptersInfo = getChaptersInfo(urlMangaName, header)
    with open("%s\\chaptersInfo.json" % urlMangaName, "w", encoding = 'utf-8') as file:
        json.dump(chaptersInfo, file, ensure_ascii = False, indent = 4)

def getTranslateBranchesInfo(url):
    urlMangaName = getUrlMangaName(url)
    if not os.path.exists("%s/chaptersInfo.json" % urlMangaName):
        return
    with open("%s/chaptersInfo.json" % urlMangaName, "r", encoding = "utf-8") as file:
        chaptersInfo = json.load(file)["data"]
    branchesInfo = []
    numbersByVolumes = []
    curVol = "1"
    numList = []
    for chapter in chaptersInfo:
        if curVol == chapter["volume"]:
            numList.append(chapter["number"])
        else:
            curVol = chapter["volume"]
            numbersByVolumes.append(numList)
            numList = []
            numList.append(chapter["number"])

        for branch in chapter["branches"]:
            idB = branch["branch_id"]
            teams = []
            for team in branch["teams"]:
                teams.append(team["name"])
            user = branch["user"]["username"]
            tempBranch = {"id": idB, "teams": teams, "user": user, "n": chapter["number"]}
            i = 0
            for branchElem in branchesInfo:
                if tempBranch["id"] == branchElem["id"]:
                    for team in tempBranch["teams"]:
                        if not team in branchElem["teams"]:
                            branchesInfo[i]["teams"].append(team)
                    if not tempBranch["user"] in branchElem["users"]:
                        branchesInfo[i]["users"].append(tempBranch["user"])
                    branchesInfo[i]["n"].append(tempBranch["n"])
                    break
                i += 1
            if i == len(branchesInfo):
                branchesInfo.append(
                    {"id": tempBranch["id"],
                     "teams": tempBranch["teams"],
                     "users": [tempBranch["user"]],
                     "n": [tempBranch["n"]]}
                )
    numbersByVolumes.append(numList)
    return branchesInfo, numbersByVolumes

def printBranchesInfo(branchesInfo):
    line = "Всего веток: %d\n" % len(branchesInfo)
    i = 1
    for branch in branchesInfo:
        lineB = "Ветка #%d\nКоманды:" % i
        for team in branch["teams"]:
            lineB += " %s; " % team
        lineB += "| Пользователи: "
        for user in branch["users"]:
            lineB += "%s; " % user
        lineB += "\nПереведены: %s" % branch["n"][0]
        extr = 0
        for j in range(1, len(branch["n"])):
            if branch["n"][j].isdigit():
                if int(branch["n"][j]) - int(branch["n"][j - 1].split(".")[0]) == 1:
                    continue
                else:
                    if j + 1 < len(branch["n"]) - 1:
                        lineB += "..%s, %s" % (branch["n"][j], branch["n"][j + 1].split(".")[0])
                    else:
                        break
            else:
                extr += 1
        lineB += "..%s" % branch["n"][-1].split(".")[0]
        if extr > 0:
            lineB += " + %d экстра" % extr
        line += lineB + "\n"
        i += 1
    print(line)

def userBranchSelection(branchAmount):
    while True:
        num = input("Выберите ветку: ")
        if not num.isdigit():
            print("Ошибка: введите цифру")
            continue
        if int(num) > branchAmount or int(num) < branchAmount:
            print("Ошибка: введите цифру в диапазоне от %d до %d" % (1, branchAmount))
            continue
        break
    return int(num)

def dowloadChapters(url, branchInfo, numbersByVolumes):
    urlMangaName = getUrlMangaName(url)
    url = "https://api.cdnlibs.org/api/manga/%s/chapter" % urlMangaName
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
    queryString = {}
    if branchInfo["id"]:
        queryString["branch_id"] = str(branchInfo["id"])
    for chapter in branchInfo["n"]:
        volume = "1"
        for i in range(0, len(numbersByVolumes)):
            if chapter in numbersByVolumes[i]:
                volume = str(i + 1)
                break
        queryString["number"] = chapter
        queryString["volume"] = volume
        response = requests.request("GET", url, headers = header, params = queryString)
        chapterInfo = response.json()
        savePath = "%s\\vol.%s\\chp.%s" % (urlMangaName, volume, chapter)
        if not os.path.exists(savePath):
            os.makedirs(savePath)
        j = 1
        for page in chapterInfo["data"]["pages"]:
            imgUrl = "https://img3.mixlib.me" + page["url"]
            img = requests.get(imgUrl, headers = header)
            with open("%s/vol.%s/chp.%s/%d.jpg" % (urlMangaName, volume, chapter, j), 'wb') as file:
                file.write(img.content)
            j += 1
            time.sleep(7 + int(rand.random() * 10))
        break

def main():
    # url = "https://mangalib.me/ru/manga/141625--bunsin-eulo-jadongsanyan" # Авто-охота с клонами
    # url = "https://mangalib.me/ru/manga/12668--dwaejiuri-" # Свинарник
    url = "https://mangalib.me/ru/manga/214416--monokuro-no-futari" # Монохромная пара
    # url = "https://mangalib.me/ru/manga/57093--aisha" # Айша
    collectMangaInfo(url)
    branchesInfo, numbersByVolumes = getTranslateBranchesInfo(url)
    printBranchesInfo(branchesInfo)
    branchIndx = 1
    if len(branchesInfo) > 1:
        branchIndx = userBranchSelection(len(branchesInfo))
    dowloadChapters(url, branchesInfo[branchIndx - 1], numbersByVolumes)

if __name__ == "__main__":
    main()