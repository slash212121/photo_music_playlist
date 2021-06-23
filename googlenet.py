import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
import torchvision.models as models
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import glob
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

device = "cuda" if torch.cuda.is_available() else "cpu" 

PATH = '/home/siyoung/photo_music/model/best_model.pt' ## 해당 경로는 저장된 모델이 담겨 있는 경로로 알맞게 변형이 필요할 듯합니다.

class Googlenet(nn.Module):
    def __init__(self, n_classes):
        super().__init__()
        googlenet = models.googlenet(pretrained=True)
        googlenet.fc = nn.Sequential(
            nn.Dropout(p=0.2),
            nn.Linear(in_features=googlenet.fc.in_features, out_features=n_classes)
        )
        self.base_model = googlenet
        self.sigm = nn.Sigmoid()

    def forward(self, x):
        return self.sigm(self.base_model(x))

model = Googlenet(5)

checkpoint = torch.load(PATH, map_location=device)
state_dict = checkpoint.get('net')
model.load_state_dict(state_dict, strict=True)

transform =  transforms.Compose([
        transforms.Resize([224, 224]),
        transforms.ToTensor(),
    ])

test_image = Image.open('/home/siyoung/photo_music/model/sinchon.jpg') ## 시험삼아 로컬에 있는 이미지를 가져왔습니다. Django의 구조에 맞게 수정해야 할듯합니다.
test_image = transform(test_image)
test_image = test_image.unsqueeze(-4)
predictions = model(test_image)
print(predictions)
