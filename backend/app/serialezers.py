from rest_framework import serializers
from .models import *

class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')


class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('__all__')


class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('__all__')

class WilayaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Wilaya
        fields = ('__all__')

class CommuneSerializers(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = ('__all__')

class DiscussionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = ('__all__')

class MessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('__all__')