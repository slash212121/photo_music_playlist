import numpy as np
import pandas as pd

origin_feelings = ['고백', '그리움', '기분전환', '멘붕/불안', 
                   '사랑/기쁨', '새벽감성', '설렘/심쿵', '스트레스/짜증', 
                   '싱숭생숭', '썸 탈때', '외로울때', '우울할때', 
                   '울고 싶을때', '이별/슬픔', '지치고 힘들때', '힐링']
new_feelings = ['love', 'enjoy', 'sentimental', 'sad', 'stressed']

origin_to_new = {
    ('고백', '사랑/기쁨', '설렘/심쿵', '썸 탈때'): 'love', 
    ('기분전환', '힐링'): 'enjoy',
    ('그리움', '싱숭생숭', '새벽감성'): 'sentimental',
    ('외로울때', '우울할때', '울고 싶을때', '이별/슬픔', '지치고 힘들때'): 'sad',
    ('멘붕/불안', '스트레스/짜증'): 'stressed'
}

music = pd.read_csv('data/music.csv')
file_name = 'data/music_category5.csv'


def merge_music(music: pd.DataFrame, origin_to_new: dict):
    music_new = music.copy()
    for keys, v in origin_to_new.items():
        col = np.zeros((len(music), ))
        for key in keys:
            col += music[key].values
            del music_new[key]
        music_new[v] = col
        music_new[v] = music_new[v].apply(lambda x: min(1, x)).astype(np.uint8)
    return music_new

def main():
    music_new = merge_music(music, origin_to_new)
    music_new.to_csv(file_name, encoding='utf-8', index=False)


if __name__ == "__main__":
    main()