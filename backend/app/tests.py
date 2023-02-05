from django.test import TestCase
from .models import *
from django.contrib.auth.models import User
# Create your tests here.


class test_adress(TestCase):
    def test_create_adress(self):
        wil = Wilaya.objects.create(name="El Bayadh")
        com = Commune.objects.create(name="Bougtoub",wilaya=wil)
        adr = Adress.objects.create(lat=34.041821,long=0.086760,commune=com)
        adr.save()

        self.assertEqual(str(adr),"Bougtoub")


class test_user(TestCase):
    def test_create_user(self):
        user = User.objects.create(username="merwan",email="merwan@gmail.com")
        user.save()

        self.assertEqual(str(user),"merwan@gmail.com")

class test_post(TestCase):
    def test_create_user(self):
        wil = Wilaya.objects.create(name="El Bayadh")
        com = Commune.objects.create(name="Bougtoub",wilaya=wil)
        adr = Adress.objects.create(lat=34.041821,long=0.086760,commune=com)
        adr.save()

        user = User.objects.create(username="merwan",email="merwan@gmail.com")
        user.save()

        post = Post.objects.create(
            user = user,
            category = "Vente",
            type = "Appartement",
            surface = 300,
            description = "description",
            prix = 100000,
            adress = adr
        )
        post.save()

        self.assertEqual(str(post),"1")