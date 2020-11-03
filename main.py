import json
import os
from contextlib import closing
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


headers = {
    'Referer': 'https://store.line.me/'
}
# proxies = {
#     'http': 'http://127.0.0.1:1087',
#     'https': 'https://127.0.0.1:1087'
# }


class Sticker(object):
    def __init__(self):
        self.status = False
        self.url = 'https://store.line.me/stickershop/product/'
        self.sticker_id = 0
        self.sticker_name = ''
        self.author = ''
        self.describe = ''
        self.sticker_list = []

    def set_sticker(self, sticker_id):
        self.sticker_id = sticker_id

    def get_sticker_info(self):
        url = self.url + self.sticker_id
        try:
            # r = requests.get(url=url, headers=headers, proxies=proxies)
            r = requests.get(url=url, headers=headers)
            bs = BeautifulSoup(r.text, 'html.parser')
            self.sticker_name = bs.find('p', class_='mdCMN38Item01Ttl').text
            self.author = bs.find('a', class_='mdCMN38Item01Author').text
            self.describe = bs.find('p', class_='mdCMN38Item01Txt').text
            items = bs.find_all('li', class_='mdCMN09Li FnStickerPreviewItem')
            for item in items:
                data = json.loads(item.get('data-preview'))
                sticker_item = {
                    'id': data.get('id'),
                    'url': data.get('staticUrl')
                }
                self.sticker_list.append(sticker_item)
            self.status = True
        except Exception as e:
            print('Cannot get sticker info.')


def check_sticker_info(sticker):
    print()
    print('---- your choice ----')
    print('id:', sticker.sticker_id)
    print('name:', sticker.sticker_name)
    print('author:', sticker.author)
    print('describe:', sticker.describe)
    print('---------------------')
    return input('Proceed? (y/n): ')


def download_sticker(sticker):
    dir_path = sticker.sticker_name
    if dir_path not in os.listdir('.'):
        os.mkdir(dir_path)
    for sticker_item in tqdm(sticker.sticker_list):
        item_id = sticker_item.get('id')
        item_url = sticker_item.get('url')
        file_path = os.path.join(dir_path, f'{item_id}.png')
        # with closing(requests.get(url=item_url, headers=headers, proxies=proxies, stream=True)) as response:
        with closing(requests.get(url=item_url, headers=headers, stream=True)) as response:
            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    for data in response.iter_content(chunk_size=1024):
                        file.write(data)
    print('Downloaded.')


if __name__ == '__main__':
    while True:
        sticker = Sticker()
        sticker.set_sticker(input('Enter sticker id: '))
        sticker.get_sticker_info()
        if sticker.status and check_sticker_info(sticker) == 'y':
            break
        print()
    download_sticker(sticker)

