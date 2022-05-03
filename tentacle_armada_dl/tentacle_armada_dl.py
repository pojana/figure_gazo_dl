import requests
# from urllib import request
import pathlib
from bs4 import BeautifulSoup
import sys
import re
import pprint
import os

# url = "https://www.sankakucomplex.com/2019/09/12/naughty-nyotengu-cosplay-by-saku-palatially-descends/"
src_url = ''
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
}

def_save_path = 'H:\\いろいろ\\_downloader\\fig_down\\'


def scrape(url, save_path):

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    title = soup.find('title').text
    title = re.sub(r'[\\|/|:|?|.|"|<|>|\|\n|]', '-', title)
    print(pathlib.Path(save_path + title))

    # pathlib.Path(save_path + title).mkdir(exist_ok=True)

    # src_iml = soup.find("div", class_='entry-content')
    # src_iml = src_iml.find_all('a')
    entry = soup.find('div', class_='entry-content')
    img_list = [i.get('href') for i in entry.find_all('a')]
    
    # print(len(img_list))

    save_img(img_list, title=title, save_path=save_path)


def save_img(url_list, title, save_path):
    pathlib.Path(save_path + title).mkdir(exist_ok=True)
    img_list = []

    for u in url_list:
        if u is None or '.jpg' not in u and '.png' not in u:
            # print('pass: {}'.format(u))
            continue
        else:
            img_list.append(u)
    
    num = len(img_list)

    for i, u in enumerate(img_list):
        # if u is None:

        u = 'https:' + u if 'http' not in u else u
        img = requests.get(u)

        print('{} / {}  response : {} url:{}'.format(str(i + 1), str(num), str(img), str(u)))

        # if True:
        if 'jlist' not in u:
            file_name = str(i + 1) + '_' + os.path.basename(u)
            with open(save_path + str(title) + str('\\') + str(file_name), 'wb') as file:
                file.write(img.content)
        else:
            pass


def main():
    args = sys.argv

    if len(args) >= 2:
        if '.txt' in args[1]:
            print('get multiple')

            add_path = args[1].replace('.txt', '')
            save_ph = def_save_path + '_' + add_path + '\\'
            print(save_ph)
            pathlib.Path(save_ph).mkdir(exist_ok=True)

            with open(args[1], mode='r', encoding='utf-8') as file:
                f = file.readlines()
                f = [li.rstrip() for li in f]
                # print(f)

                for i, line in enumerate(f):
                    print('{} / {} scrape_url:{}'.format(str(i), str(len(f)), str(line)))
                    scrape(line, save_path=save_ph)
                    i += 1
        else:
            print('get one url')
            scrape(args[1], def_save_path)
    else:
        print('please url or urlList.txt')


if __name__ == '__main__':
    main()