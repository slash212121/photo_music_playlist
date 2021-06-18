import os
import flickrapi
from skimage import io

api_key = u'd940dedd0800469dc9583c1964d3837b'
api_secret = u'b8f61718b615bb8e'
flickr = flickrapi.FlickrAPI(api_key, api_secret, cache=True)

# 키워드는 바꾸기 가능
keywords = ['love', 'enjoy', 'sentimental', 'sad', 'stressed']
# 이미지 개수도 바꾸기 가능
n_max = 10


def collect_urls_by_keyword(keyword: str, n_max: int):
    """Collect urls of images by keyword using flickr api """
    photos = flickr.walk(
        text=keyword,
        tag_mode='all',
        tags=keyword,
        extras='url_c',
        per_page=100,           
        sort='relevance'
    )
    
    cnt = 0
    urls = []
    while cnt < n_max:
        photo = next(photos)
        url = photo.get('url_c')
        if url is not None:
            urls.append(url)
            cnt += 1
    return urls

def get_images_from_urls(urls):
    """Read images from urls"""
    return [io.imread(url) for url in urls]

def save_images(images, prefix, path):
    """Save images to file"""
    for i, img in enumerate(images):
        io.imsave(os.path.join(path, prefix + str(i) + '.jpg'), img)

def main():
    for keyword in keywords:
        path = os.path.join('./data/images', keyword)
        if not os.path.exists(path):
            os.mkdir(path)
        urls = collect_urls_by_keyword(keyword, n_max)
        images = get_images_from_urls(urls)
        save_images(images, 'flickr', path)


if __name__ == "__main__":
    main()