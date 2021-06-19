import os
import requests

from get_images_flickr import keywords, get_images_from_urls, save_images

# 키워드는 바꾸기 가능
keywords = ['love', 'enjoy', 'sentimental', 'sad', 'stressed']
# 페이지 개수
page_num = 1
# 이미지 개수도 바꾸기 가능
n_max = 10


def collect_urls_by_keyword(keyword: str, page_num: int, n_max: int, scenery: bool = False):
    """Collect urls of images by keyword using splash api """
    if scenery:
        keyword += '-scenery'
    r = requests.get(f'https://api.unsplash.com/search/collections?query={keyword}&page={page_num}&per_page={n_max}&client_id=1H5zbugfvk1UOnX60y2yiMyjNMrE-vdpThxGkP1y9_E')
    data = r.json()
    results = data['results']
    urls = [res['cover_photo']['urls']['raw'] for res in results]
    return urls

def main():
    for keyword in keywords:
        path = os.path.join('./data/images', keyword)
        if not os.path.exists(path):
            os.mkdir(path)
        urls = collect_urls_by_keyword(keyword, page_num, n_max)
        images = get_images_from_urls(urls)
        save_images(images, 'unsplash', path)


if __name__ == "__main__":
    main()