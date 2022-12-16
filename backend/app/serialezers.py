from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        token['email'] = user.email
        return token


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('__all__')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data) 
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance



class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')


class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
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