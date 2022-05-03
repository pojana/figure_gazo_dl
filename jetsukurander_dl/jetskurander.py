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

syuum_path = 'H:\\いろいろ\\_downloader\\fig_down\\jetskurander\\'
moto_url = 'http://jetsukurander.blog37.fc2.com/blog-category-9.html'
# base_url = 'http://30calclub.sakura.ne.jp/ORCHID/'

def scrape(url, save_path):

    r = requests.get(url, headers=headers)

    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'lxml')

    title = soup.find('h2', class_='entry_header').text
    title = re.sub(r'[1-9]/[1-9]', '', title).replace('　　', ' ')
    title = re.sub(r'[\\|/|:|?|.|"|<|>|\|\n|]', '-', title)
    title = replace_fileName(title=title)
    title = title.replace('　', '').strip()
    print(pathlib.Path(save_path + title))

    # pathlib.Path(save_path + title).mkdir(exist_ok=True)

    # src_iml = soup.find_all("div", class_='EntryText')[-1]
    entry = soup.find('div', class_='entry_body')
    img_list = [s.get('href') for s in entry.find_all('a')]
    
    # sentry = soup.find('div', class_='main-inner')
    # print(entry)

    # img_list = [i.get('src') for i in src_iml]
    
    # print(img_list)

    # img_base_url = url.replace(os.path.basename(url), '')
    # img_list = [img_base_url + i for i in img_list]

    save_img(img_list, title=title, save_path=save_path)


def save_img(url_list, title, save_path):
    pathlib.Path(save_path + title).mkdir(exist_ok=True)
    img_list = []

    for u in url_list:
        if u is None or '.jpg' not in u and '.png' not in u and '.JPG' not in u:
            # print('pass: {}'.format(u))
            continue
        else:
            img_list.append(u)
    
    num = len(img_list)
    # print(img_list)

    for i, u in enumerate(img_list):
        # if u is None:

        u = 'https:' + u if 'http' not in u else u
        try:
            img = requests.get(u, headers=headers)
        except:
            continue

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

    src = soup.find_all('h2', class_='entry_header')
    # print(src)
    # url_list = [s.find('a').get('href') for s in src]
    url_list = [s.find('a').get('href') for s in src]
    # url_list = [s for s in url_list if s != 'http://sh1nku.blog.fc2.com/blog-category-0.html']

    next = soup.find('a', title='次のページ')
    
    if next is None:
        pass
    else:
        next_url = src_url + next.get('href')
        print("next: {}".format(next_url))
        # print("{}".format(url_list))
        url_list.extend(get_download_page_list(next_url))

    return url_list


def download_img_from_urlList(down_list, save_path):
    for i, line in enumerate(down_list):
        print('{} / {} scrape_url:{}'.format(str(i), str(len(down_list)), str(line)))
        # if i <= 944:
        #     continue
        scrape(line, save_path=save_path)
        i += 1


def replace_fileName(title):
    re.sub(r'[\\|/|:|?|.|!|*|"|<|>|\|]', '_', title)
    replace_table = ['\\', '"', '*', "?", ":", "|", "<", ">", "/"]
    for rep in replace_table:
        title = title.replace(rep, '_')
        title = title.replace(rep, '_')
        title = title.replace(rep, '_')

        title = title.replace(chr(92), '_')
    return title


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

            download_img_from_urlList(f, save_path=syuum_path)

        else:
            print('get one url')
            pathlib.Path(syuum_path).mkdir(exist_ok=True)
            scrape(args[1], syuum_path)
    else:
        print('please url or urlList.txt')

        pathlib.Path(syuum_path).mkdir(exist_ok=True)
        dl_list = get_download_page_list(moto_url)
        print(dl_list)
        download_img_from_urlList(dl_list, save_path=syuum_path)


if __name__ == '__main__':
    main()