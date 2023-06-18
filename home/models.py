from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class MusicFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='music/')
    privacy = models.CharField(max_length=10,default='public')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)

class AllowedUser(models.Model):
    music_file = models.ForeignKey(MusicFile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    