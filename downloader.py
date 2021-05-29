# Import needed packages
import flickrapi
import urllib
from PIL import Image

# Information to access Flickr API
api_key = u'd940dedd0800469dc9583c1964d3837b'
api_secret = u'b8f61718b615bb8e'

# Flickr api access key 
flickr=flickrapi.FlickrAPI(api_key, api_secret, cache=True)

# Options to search for in Flickr API
N_MAX = int(input('Enter Maximum number of images: '))
keyword = input('Enter the keyword to search in Flickr: ')
directory = input('Enter the directory to save images: ')
RESIZE_OPTION = Image.ANTIALIAS


# Searching for images via API
photos = flickr.walk(text=keyword,
                     tag_mode='all',
                     tags=keyword,
                     extras='url_c',
                     per_page=100,           # may be you can try different numbers..
                     sort='relevance')

# Get list of the URL's of the searched images
urls = []
for i, photo in enumerate(photos):
    print (i)
    
    url = photo.get('url_c')
    urls.append(url)
    
    # get 50 urls
    if i > N_MAX:
        break
  
#Get rid of None values
urls = filter(None.__ne__, urls)
urls = list(urls)

for i in range(len(urls)):
  fname = f'img_{keyword}_{i}.jpg'
  url = urls[i]
  urllib.request.urlretrieve(url,fname)
  # Resize the image and overwrite it
  image = Image.open(f'{fname}') 
  image = image.resize((256, 256), RESIZE_OPTION)
  image.save(f'{directory}/{fname}')