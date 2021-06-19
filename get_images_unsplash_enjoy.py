#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import requests

from get_images_flickr import get_images_from_urls, save_images

# 키워드는 바꾸기 가능
keywords = ['enjoy']
# 페이지 개수
data_size = 1000
# 이미지 개수도 바꾸기 가능
n_max = 30


def collect_urls_by_keyword(keyword: str, n_max: int, scenery: bool = False):
    """Collect urls of images by keyword using splash api """
    if scenery:
        keyword += '-scenery'
    urls = []
    for i in range(1, data_size // n_max + 2):
        r = requests.get(f'https://api.unsplash.com/search/collections?query={keyword}&page={i}&per_page={n_max}&client_id=1H5zbugfvk1UOnX60y2yiMyjNMrE-vdpThxGkP1y9_E')
        data = r.json()
        results = data['results']
        urls += [res['cover_photo']['urls']['raw'] for res in results]
        print(i, len(urls))
    return urls

def main():
    for keyword in keywords:
        path = os.path.join('./data/images', keyword)
        if not os.path.exists(path):
            os.mkdir(path)
        urls = collect_urls_by_keyword(keyword, n_max)
        images = get_images_from_urls(urls)
        save_images(images, 'unsplash', path)


if __name__ == "__main__":
    main()

