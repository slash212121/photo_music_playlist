from django.shortcuts import render
from website.settings import MEDIA_ROOT

import os
import json
import numpy as np
import urllib
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
import io
from PIL import Image

from playlist.models import Music

class Resnext50(nn.Module):
    def __init__(self, n_classes):
        super().__init__()
        resnet = models.resnext50_32x4d()
        resnet.fc = nn.Sequential(
            nn.Dropout(p=0.2),
            nn.Linear(in_features=resnet.fc.in_features, out_features=n_classes)
        )
        self.base_model = resnet
        self.sigm = nn.Sigmoid()

    def forward(self, x):
        return self.sigm(self.base_model(x))

# Create your views here.
def index(request):
    return render(request, 'playlist/index_copy.html')

def to_index(request):
    return render(request, 'playlist/index.html')
# 6.24 혜연 : 수빈님 바뀐 html에 맞춰서 list.html을 index_old.html로 수정해야 함. (혹은 index_old 명을 변경)

def recommend(request):
    image = request.FILES['imageUpload']
    image_arr = _grab_image(stream=image)
    image_save = Image.fromarray(image_arr)
    # 사용자로부터 받은 이미지 저장
    image_save.save(os.path.join(MEDIA_ROOT, 'temp.png'))
    ############ model part ###########
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_path = 'best_model.pth'
    checkpoint = torch.load(model_path, map_location=device)
    state_dict = checkpoint.get('net')
    transform = transforms.Compose([
        transforms.Resize([256, 256]),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    img = transform(image_save).unsqueeze(0).to(device).double()
    model = Resnext50(5)
    model = model.to(device).double()
    model.load_state_dict(state_dict, strict=True)
    pred = model(img)
    print(pred)
    ###################################
    # temporary output
    results = list(Music.objects.all()[:10])
    results = [
        {'artist_name': r.artist_name, 'music_name': r.music_name} \
        for r in results 
    ]
    results = json.dumps(results)
    return render(request, 'playlist/list.html', {'results': results})
# 6.24 혜연 : 수빈님 바뀐 html에 맞춰서 list.html을 index_old.html로 수정해야 함. (혹은 index_old 명을 변경)

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