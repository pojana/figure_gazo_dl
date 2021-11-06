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

syuum_path = 'H:\\いろいろ\\figs\\shonboriegao\\'
moto_url = 'https://syonboriegao.wixsite.com/figroku/review'


def scrape(url, save_path):

    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'lxml')

    title_temp = soup.find_all('span', class_='_2PHJq public-DraftStyleDefault-ltr')
    maker_temp = [t.text for t in title_temp if 'メーカー' in t.text]
    title_temp = [t.text for t in title_temp if '商品名' in t.text]
    
    if maker_temp == []:
        title = ''
    else:
        title = maker_temp[0].split('：')[-1] + ' '

    if title_temp == []:
        # print(soup)
        print(r)
        with open('errlog.txt', 'w') as f:
            f.write(str(soup))
        print(url)
        title += soup.find('title').text.replace('『', '').replace('』 ', '')
    else:
        title += title_temp[0].replace('商品名', '').strip().replace('：', '')

    pprint.pprint(title)

    title = re.sub(r'[\\|/|:|?|.|"|<|>|\|\n|*|]', '-', title)
    print(pathlib.Path(save_path + title))

    src_iml = soup.find("div", class_='bVAkx _3777I _1dQP3')
    src_iml = src_iml.find_all('img')

    # print(src_iml)
    # sentry = soup.find('div', class_='main-inner')
    # print(entry)

    img_list = [i.get('src').split('/v1/fit')[0] for i in src_iml]
    print(img_list)
    
    # print(len(img_list))

    save_img(img_list, title=title, save_path=save_path)


def save_img(url_list, title, save_path):
    pathlib.Path(save_path + title).mkdir(exist_ok=True)
    img_list = url_list
    
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


def get_download_page_list(url):

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    # print(soup)

    src = soup.find('div', class_='pro-gallery')
    src = src.find_all('a')
    # print(src)
    url_list = [s.get('href') for s in src if s.get('href') is not None]
    # url_list = [s.get('href') for s in soup.find_all('a', class_='read-more-link')]
    # print(url_list)

    next = soup.find('a', attrs={'data-hook': "pagination__next"})

    if next is None:
        pass
    else:
        next_url = src_url + next.get('href')
        print('next_url: {}'.format(next_url))
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
        pprint.pprint(dl_list)
        print(len(dl_list))
        download_img_from_urlList(dl_list, save_path=syuum_path)


if __name__ == '__main__':
    main()