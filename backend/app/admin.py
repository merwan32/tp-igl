from django.contrib import admin
from .models import Post,Profile,Image
from django.contrib.auth.models import Group

# Register your models here.

admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Profile)
admin.site.unregister(Group)