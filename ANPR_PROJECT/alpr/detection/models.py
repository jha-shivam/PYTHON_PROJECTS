from django.db import models
from django.utils import timezone
# Create your models here.
class Images(models.Model):
    photo = models.ImageField(default='profile.png',upload_to='images')
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return '%s' % (self.photo)
    

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name