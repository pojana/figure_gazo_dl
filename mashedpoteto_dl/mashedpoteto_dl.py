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



def_save_path = 'H:\\いろいろ\\_downloader\\fig_down\\mashedpoteto\\'

base_url = 'https://www.mashedpopoto.com'
src_url = 'https://www.mashedpopoto.com/category/anime-figures'

def scrape(url, save_path):

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    title = soup.find('h1', class_='blog-post-main-title').text
    title = re.sub(r'[\\|/|:|?|.|"|<|>|\|\n|]', '-', title).strip()
    print(pathlib.Path(save_path + title))

    # pathlib.Path(save_path + title).mkdir(exist_ok=True)

    # src_iml = soup.find("div", class_='entry-content')
    # src_iml = src_iml.find_all('a')
    entry = soup.find('div', class_='blog-content-block')
    # print(entry)

    img_list = [i.get('src') for i in entry.find_all('img')]
    
    first = entry.find('div', class_='w-dyn-list')
    first_img = first.find('img').get('src')
    
    img_list.insert(0, first_img)

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

    src = soup.find('div', class_='blog-list-wrapper w-dyn-list')
    url_list = src.find_all('div', role='listitem')
    url_list = [u.find_all('a')[-1].get('href') for u in url_list]
    url_list = [base_url + u for u in url_list]
    # print(url_list)

    next = src.find('div', role='navigation')
    next = next.find('a', attrs={'aria-label': 'Next Page'})
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
    pathlib.Path(def_save_path).mkdir(exist_ok=True)

    if len(args) >= 2:
        if '.txt' in args[1]:
            print('get multiple')

            add_path = args[1].replace('.txt', '').replace('.\\', '').strip()
            save_ph = def_save_path + '_' + add_path + '\\'
            print(save_ph)
            pathlib.Path(save_ph).mkdir(exist_ok=True)

            with open(args[1], mode='r', encoding='utf-8') as file:
                f = file.readlines()
                f = [li.rstrip() for li in f]
            
            download_img_from_urlList(f, save_path=save_ph)
            
        else:
            print('get one url')
            scrape(args[1], def_save_path)
    else:
        print('please url or urlList.txt')
        dl_list = get_download_page_list(src_url)
        download_img_from_urlList(dl_list, def_save_path)


if __name__ == '__main__':
    main()