from django.shortcuts import render
from website.settings import MEDIA_ROOT

import os
import numpy as np
import urllib
import io
from PIL import Image

# Create your views here.
def index(request):
    return render(request, 'playlist/index.html')

def recommend(request):
    image = request.FILES['imageUpload']
    image_arr = _grab_image(stream=image)
    image_save = Image.fromarray(image_arr)
    # 사용자로부터 받은 이미지 저장
    image_save.save(os.path.join(MEDIA_ROOT, 'temp.png'))
    return render(request, 'playlist/list.html')

def _grab_image(path=None, stream=None, url=None):
    # if the path is not None, then load the image from disk
    image = None
    if path is not None:
        image = Image.open(path)
	# otherwise, the image does not reside on disk
    else:	
		# if the URL is not None, then download the image
        if url is not None:
            resp = urllib.urlopen(url)
            data = resp.read()
		# if the stream is not None, then the image has been uploaded
        elif stream is not None:
            data = stream.read()
		# convert the image to a NumPy array and then read it into
        bytearr = bytearray(data)
        image = Image.open(io.BytesIO(bytearr))
    image = np.asarray(image)
    return image