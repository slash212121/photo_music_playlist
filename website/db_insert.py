import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from playlist.models import Music
import pandas as pd

def insert_data():
    objs = Music.objects.all()
    data = pd.read_csv('../data/music_category5.csv')
    if len(objs) == len(data):
        print("Nothing to insert!")
    else:
        for i, row in data.iterrows():
            music_id = row['music_ID']
            artist_name = row['artist_disp_nm']
            music_name = row['track_title']
            love = row['love']
            enjoy = row['enjoy']
            sentimental = row['sentimental']
            sad = row['sad']
            stressed = row['stressed']
            music = Music(music_id=music_id, artist_name=artist_name, music_name=music_name,
                          love=love, enjoy=enjoy, sentimental=sentimental, 
                          sad=sad, stressed=stressed)
            music.save()
            print("%dth is done." % i)
        print("All saved!")


if __name__ == "__main__":
    insert_data()