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

syuum_path = 'H:\\いろいろ\\_downloader\\fig_down\\楽園 フィギュア レビュー ブログ\\'
moto_url = 'https://syuumie.hatenablog.com/search?q=R18'


def scrape(url, save_path):

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    title = soup.find('title').text.replace('【R18】', '').replace('- 楽❚園 　　フィギュア レビュー ブログ', '')
    title = re.sub(r'[\\|/|:|?|.|"|<|>|\|\n|]', '-', title)
    title = title.strip()
    print(pathlib.Path(save_path + title))

    # pathlib.Path(save_path + title).mkdir(exist_ok=True)

    # src_iml = soup.find("div", class_='entry-content')
    # src_iml = src_iml.find_all('a')
    entry = soup.find('div', class_='entry-content')
    # print(entry)

    img_list = [i.get('src') for i in entry.find_all('img')]
    
    # print(len(img_list))

    save_img(img_list, title=title, save_path=save_path)


def save_img(url_list, title, save_path):
    pathlib.Path(save_path + title).mkdir(exist_ok=True)
    
    num = len(url_list)

    for i, u in enumerate(url_list):
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


def get_download_page_list(url):

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    src = soup.find('div', class_='archive-entries')
    url_list = src.find_all('a', class_='entry-thumb-link')
    url_list = [u.get('href') for u in url_list]
    # print(url_list)

    next = src.find('div', role='pager autopagerize_insert_before')

    if next is None:
        pass
    else:
        next_url = src_url + next.find('a').get('href')
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
            scrape(args[1], def_save_path)
    else:
        print('please url or urlList.txt')

        pathlib.Path(syuum_path).mkdir(exist_ok=True)
        dl_list = get_download_page_list(moto_url)
        download_img_from_urlList(dl_list, save_path=syuum_path)


if __name__ == '__main__':
    main()