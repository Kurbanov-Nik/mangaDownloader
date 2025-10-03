import requests

def main():
    imgUrl = ("https://img3.mixlib.me"
              "//manga/four-knights-of-the-apocalypse/chapters/3516354/36e9c392-753f-49eb-aec6-5987d9614157.jpg")

    headers = {
        'Origin' : 'https://mangalib.me',
        'Referer' : 'https://mangalib.me/ru/54750--four-knights-of-the-apocalypse/read/v21/c185'
    }


    r = requests.get(imgUrl, headers = headers)
    print(r.content)
    with open("01.jpg", 'wb') as f:
        f.write(r.content)
    # pass

if __name__ == "__main__":
    main()