from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    phone = models.IntegerField()
    profile_picture = models.ImageField(upload_to='profilepics',default='profilepics/default-user.png')

    def __str__(self):
        return str(self.id)



CATEGORY_CHOICES = (
    ('Vente','Vente'),
    ('Echange', 'Echange'),
    ('Location','Location'),
    ('Location pour vacances','Location pour vacances'),
)


class Post(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    category = models.CharField(max_length=25 , choices=CATEGORY_CHOICES)
    type =  models.CharField(max_length=100)
    surface = models.IntegerField()
    description = models.CharField(max_length=255)
    prix = models.IntegerField()

    def __str__(self):
        return str(self.id)

class Image(models.Model):
    Post = models.ForeignKey(Post,on_delete=models.CASCADE)
    img = models.ImageField(upload_to='postimages')

    def __str__(self):
        return str(self.id)


class Wilaya(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id) +'--'+ self.name


class Commune(models.Model):
    name = models.CharField(max_length=100)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE)


class Discussion(models.Model):
    user = models.ForeignKey("Profile", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    is_closed = models.BooleanField(default=False)

class Message(models.Model):
    discussion = models.ForeignKey("Discussion", on_delete=models.CASCADE)
    sender = models.ForeignKey("Profile", on_delete=models.CASCADE)
    content = models.CharField(max_length=500)