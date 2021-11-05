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


def_save_path = 'H:\\いろいろ\\figs\\'

syuum_path = 'H:\\いろいろ\\figs\\泥の河のPLASTIC\\'
moto_url = 'http://adultfigure.blog.jp/'


def scrape(url, save_path):

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    title = soup.find('title').text.replace('[レビュー]', '')
    title = re.sub(r'[\\|/|:|?|.|"|<|>|\|\n|]', '-', title)
    title = title.strip()
    print(pathlib.Path(save_path + title))

    # pathlib.Path(save_path + title).mkdir(exist_ok=True)

    src_iml = soup.find('div', class_='entry-content')
    src_iml = src_iml.find_all('a')
    # sentry = soup.find('div', class_='main-inner')

    img_list = [i.get('href') for i in src_iml]
    print(img_list)
    
    # print(len(img_list))

    save_img(img_list, title=title, save_path=save_path)


def save_img(url_list, title, save_path):
    pathlib.Path(save_path + title).mkdir(exist_ok=True)
    img_list = []
    
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
            file_name = str(i + 1) + '_' + os.path.basename(u) + '.jpg'
            with open(save_path + str(title) + str('\\') + str(file_name), 'wb') as file:
                file.write(img.content)
        else:
            pass


def get_download_page_list(url):

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    # print(soup)

    src = soup.find_all('h1', class_='article-title')
    # print(src)
    # url_list = [s.find('a').get('href') for s in src]
    url_list = [s.find('a').get('href') for s in src]
    print(url_list)

    next = soup.find('a', rel='next')

    if next is None:
        pass
    else:
        next_url = src_url + next.get('href')
        url_list.extend(get_download_page_list(next_url))

    return url_list


def download_img_from_urlList(down_list, save_path):
    for i, line in enumerate(down_list):
        print('{} / {} scrape_url:{}'.format(str(i), str(len(down_list)), str(line)))
        scrape(line, save_path=save_path)
        i += 1


def main():
    args = sys.argv

    if len(args) >= 2:
        if '.txt' in args[1]:
            print('get multiple')

            add_path = args[1].replace('.txt', '').replace('.\\', '').strip()
            save_ph = def_save_path + add_path + '\\'
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
            pathlib.Path(syuum_path).mkdir(exist_ok=True)
            scrape(args[1], syuum_path)
    else:
        print('please url or urlList.txt')

        pathlib.Path(syuum_path).mkdir(exist_ok=True)
        dl_list = get_download_page_list(moto_url)
        download_img_from_urlList(dl_list, save_path=syuum_path)


if __name__ == '__main__':
    main()