from extraFunctions import choiceSleepTime
import re
import requests
import os
import json
import time

REQUEST_HEADERS = {
    "Client-Time-Zone": "Europe/Moscow",
    "Content-Type": "application/json",
    "Referer": "https://mangalib.me/",
    'sec-ch-ua': "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Google Chrome\";v=\"140\"",
    'sec-ch-ua-mobile': "?0",
    'sec-ch-ua-platform': "\"Windows\"",
    'Site-Id': "1",  # important field
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}
URL_MANGA_NAME = ""

def setURLMangaName(url):
    global URL_MANGA_NAME
    pattern = re.compile(r"[0-9]+-(-[a-z]+)+", re.I)
    URL_MANGA_NAME = url.split("?")[0][pattern.search(url).start():]

def setRequestHeadersParam(paramKey, paramValue):
    global REQUEST_HEADERS
    REQUEST_HEADERS[paramKey] = paramValue

def getFirstResponse(url):
    response = requests.request("GET", url = url, headers = REQUEST_HEADERS)
    return response

def getAboutInfo():
    requestParams = {
        "fields[]":
            ["background", "eng_name", "otherNames", "summary", "releaseDate", "type_id", "caution",
             "views", "close_view", "rate_avg", "rate", "genres", "tags", "teams", "user", "franchise",
             "authors", "publisher", "userRating", "moderated", "metadata", "metadata.count",
             "metadata.close_comments", "manga_status_id", "chap_count", "status_id", "artists", "format"]
    }
    url = "https://api.cdnlibs.org/api/manga/" + URL_MANGA_NAME
    response = requests.request("GET", url, headers = REQUEST_HEADERS, params = requestParams)
    return response.json()

def getChaptersInfo():
    url = "https://api.cdnlibs.org/api/manga/" + URL_MANGA_NAME + "/chapters"
    response = requests.request("GET", url, headers = REQUEST_HEADERS)
    return response.json()

def collectMangaInfo():
    url = "https://mangalib.me/ru/manga/" + URL_MANGA_NAME + "?section=info"
    response = requests.request("GET", url = url, headers = REQUEST_HEADERS)
    if not response.status_code == 200:
        print("ОШИБКА: %d код" % response.status_code)
        return
    if not os.path.exists(URL_MANGA_NAME):
        os.mkdir(URL_MANGA_NAME)
    aboutInfo = getAboutInfo()
    with open("%s\\aboutInfo.json" % URL_MANGA_NAME, "w", encoding = 'utf-8') as file:
        json.dump(aboutInfo, file, ensure_ascii = False, indent = 4)
    # Age Restriction Titles (18+) can not download, because need authorization
    if aboutInfo["data"]["ageRestriction"]["id"] == 4:
        print("Ограничение 18+ : необходима авторизация на сайте")
        return
    # header["Authorization"] = "token"
    chaptersInfo = getChaptersInfo()
    with open("%s\\chaptersInfo.json" % URL_MANGA_NAME, "w", encoding = 'utf-8') as file:
        json.dump(chaptersInfo, file, ensure_ascii = False, indent = 4)

def getTranslateBranchesInfo():
    if not os.path.exists("%s/chaptersInfo.json" % URL_MANGA_NAME):
        return
    with open("%s/chaptersInfo.json" % URL_MANGA_NAME, "r", encoding = "utf-8") as file:
        chaptersInfo = json.load(file)["data"]
    branchesInfo = {}
    allTeams = {}
    chaptersList = []
    for index, chapter in enumerate(chaptersInfo):
        chaptersList.append((chapter["volume"], chapter["number"]))
        for branch in chapter["branches"]:
            teams = []
            for team in branch["teams"]:
                teams.append(team["id"])
                allTeams[team["id"]] = team["name"]
            branchesInfo.setdefault(branch["branch_id"], []).append({
                "chapter_id": index,
                "teams": (*teams,),
                "date": branch["created_at"],
                "expired_type": branch["expired_type"]})
    return branchesInfo, chaptersList, allTeams

def printBranchesInfo(branchesInfo, chapters, allTeams):
    infoLine = "Всего веток: %d" % len(branchesInfo)
    for i, branchID in enumerate(branchesInfo):
        infoLine += "\nВетка #%d" % (i + 1)
        branchTeams = list(branchesInfo[branchID][0]["teams"])
        branchExtras = 0 if chapters[branchesInfo[branchID][0]["chapter_id"]][1].isdigit() else 1
        translated = "\nПереведены: %s" % chapters[branchesInfo[branchID][0]["chapter_id"]][1]
        for j in range(1, len(branchesInfo[branchID])):
            branchTeams.append(*branchesInfo[branchID][j]["teams"])
            prevNum = chapters[branchesInfo[branchID][j - 1]["chapter_id"]][1]
            curNum = chapters[branchesInfo[branchID][j]["chapter_id"]][1]
            if curNum.isdigit():
                if int(curNum) - int(prevNum.split(".")[0]) == 1:
                    continue
                else:
                    if j + 1 < len(branchesInfo[branchID]) - 1:
                        translated += "..%s, %s" % (prevNum.split(".")[0], curNum)
                    else:
                        break
            else:
                branchExtras += 1
        translated += "..%s" % chapters[branchesInfo[branchID][-1]["chapter_id"]][1].split(".")[0]

        branchTeams = set(branchTeams)
        infoLine += "\nКоманды: "
        for teamID in branchTeams:
            infoLine += allTeams[teamID]
        if branchExtras > 0:
            translated += " + %d экстра" % branchExtras
        infoLine += translated + "\n"
    print(infoLine)

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

def dowloadChapters(branchInfo, branchID, chaptersList):
    url = "https://api.cdnlibs.org/api/manga/%s/chapter" % URL_MANGA_NAME
    requestParams = {}
    if branchID:
        requestParams["branch_id"] = str(branchID)
    for chapter in branchInfo:
        requestParams["number"] = chaptersList[chapter["chapter_id"]][1]
        requestParams["volume"] = chaptersList[chapter["chapter_id"]][0]
        response = requests.request("GET", url, headers = REQUEST_HEADERS, params = requestParams)
        chapterInfo = response.json()
        savePath = "%s\\vol.%s\\chp.%s" % (URL_MANGA_NAME, requestParams["volume"], requestParams["number"])
        if not os.path.exists(savePath):
            os.makedirs(savePath)
        for j, page in enumerate(chapterInfo["data"]["pages"]):
            imgUrl = "https://img3.mixlib.me" + page["url"]
            img = requests.get(imgUrl, headers = REQUEST_HEADERS)
            with open("%s/vol.%s/chp.%s/%d.jpg" % (URL_MANGA_NAME, requestParams["volume"], requestParams["number"], j + 1), 'wb') as file:
                file.write(img.content)
            timeSleep = choiceSleepTime()
            print("[✔] vol.%s chp.%s p.%d | Now sleep: %.2f sec" % (requestParams["volume"], requestParams["number"], j + 1, timeSleep))
            time.sleep(timeSleep)
        break

def main():
    url = "https://mangalib.me/ru/manga/214416--monokuro-no-futari"
    setURLMangaName(url)
    collectMangaInfo()
    branchesInfo, chaptersList, allTeams = getTranslateBranchesInfo()
    printBranchesInfo(branchesInfo, chaptersList, allTeams)
    branches = []
    for key in branchesInfo:
        branches.append(key)
    branchIndx = 1
    if len(branchesInfo) > 1:
        branchIndx = userBranchSelection(len(branchesInfo))
    dowloadChapters(branchesInfo[branches[branchIndx - 1]], branches[branchIndx - 1], chaptersList)

if __name__ == "__main__":
    main()