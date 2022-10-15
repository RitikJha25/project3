from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User

class editor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ScriptName = models.CharField(max_length=50, blank=  True, null= True)
    bodyTxt = HTMLField(blank=  True, null= True)


class ConversionEditor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ScriptName = models.CharField(max_length=50, blank=  True, null= True)
    bodyTxt = HTMLField(blank=  True, null= True)



class ScriptToEdit(models.Model):
    script = models.FileField(upload_to="script_Editor/userScripts")
    dateCreated = models.DateField(auto_now_add = True)
    class Meta:
        db_table = "Scripts"



class FeedBack(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add = True)
    FormId = models.AutoField(primary_key=True)
    RateValue = models.CharField(max_length=50)
    Name = models.CharField(max_length=30)
    Email = models.CharField(max_length=50)
    Description = models.CharField(max_length=500)
    RateNarration = models.CharField(default="", max_length=20)
    RateConversion = models.CharField(default="", max_length=20)
    
