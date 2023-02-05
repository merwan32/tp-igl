from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Wilaya(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id) +'--'+ self.name


class Commune(models.Model):
    name = models.CharField(max_length=100)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
    


class Adress(models.Model):
    lat = models.FloatField()
    long = models.FloatField()
    commune = models.ForeignKey(Commune,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.commune.name)


class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length=25 )
    type =  models.CharField(max_length=100)
    surface = models.IntegerField()
    description = models.CharField(max_length=1000)
    prix = models.IntegerField()
    adress = models.ForeignKey(Adress,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)
    
class Offre(models.Model):
   sender = models.ForeignKey(User,on_delete=models.CASCADE, related_name='sender')
   reciver = models.ForeignKey(User,on_delete=models.CASCADE, related_name='receiver')
   post =  models.ForeignKey(Post,on_delete=models.CASCADE)
   phone = models.IntegerField()
   prix = models.IntegerField()
   description = models.CharField(max_length=1000)

   def __str__(self):
        return str(self.id)



class Image(models.Model):
    Post = models.ForeignKey(Post,on_delete=models.CASCADE)
    img = models.ImageField(upload_to='postimages')

    def __str__(self):
        return str(self.id)


class Discussion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_closed = models.BooleanField(default=False)

class Message(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)