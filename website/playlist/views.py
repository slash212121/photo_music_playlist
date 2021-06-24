from django.shortcuts import render
from website.settings import MEDIA_ROOT
from playlist.models import Music

import os
from random import shuffle
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
    pred = model(img).detach().numpy().squeeze()
    ###################################
    # temporary output
    # results = list(Music.objects.all()[:10])
    # 추천
    results = _recommend(pred)
    results = [
        {'artist_name': r.artist_name, 'music_name': r.music_name} \
        for r in results
    ]
    results = json.dumps(results)
    return render(request, 'playlist/list.html', {'results': results})

def _recommend(arr):
    # sad, sentimental index 확인 필요!!!
    emotions_to_int = {'love': 0, 'enjoy': 1, 'sad': 2, 'sentimental': 3, 'stressed': 4}
    int_to_emotions = {v: k for k, v in emotions_to_int.items()}
    dominant_emotion = int_to_emotions[np.argmax(arr)]
    print(dominant_emotion)
    # fetch all
    musics = list(Music.objects.all())
    # fetch musics with dominant emotion
    # musics = [m for m in musics if getattr(m, dominant_emotion) == 1]
    # key: music_id, value: score
    musics_score = {m.music_id: [0, 1] for m in musics}
    # sub_emotions = [e for e in emotions_to_int.keys() if e != dominant_emotion]
    emotions = [e for e in emotions_to_int.keys()]
    for m in musics:
        for e in emotions:
            if getattr(m, e) == 1:
                musics_score[m.music_id][0] += arr[emotions_to_int[e]]
                musics_score[m.music_id][1] += 1
    shuffle(musics)
    musics.sort(key=lambda x: -musics_score[x.music_id][0] / musics_score[x.music_id][1])
    musics = musics[:20]
    return musics

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
        image = Image.open(io.BytesIO(bytearr)).convert('RGB')
    image = np.asarray(image)
    return image
