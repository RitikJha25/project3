from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to = "profile_pic" )

    def __str__(self):
        return f'{self.user.username} profile'



class ReferUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    referId =models.CharField(max_length=100, blank=True)
    refferedBy = models.CharField(max_length=100, blank= True)
    totalRefferals = models.IntegerField()





