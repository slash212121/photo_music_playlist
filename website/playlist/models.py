from django.db import models

max_length = 200

# Create your models here.
class Music(models.Model):
    music_id = models.IntegerField(primary_key=True)
    artist_name = models.CharField(max_length=max_length)
    music_name = models.CharField(max_length=max_length)
    love = models.PositiveSmallIntegerField()
    enjoy = models.PositiveSmallIntegerField()
    sentimental = models.PositiveSmallIntegerField()
    sad = models.PositiveSmallIntegerField()
    stressed = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"[{self.music_id}] {self.artist_name}: {self.music_name}"