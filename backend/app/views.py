from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serialezers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.serializers import SocialLoginSerializer
from google.oauth2 import id_token
from google.auth import transport
import requests
import json


# Create your views here.

class GoogleView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        token = {'id_token': request.data.get('id_token')}

        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token['id_token'], transport.requests.Request(), '938713439568-q7barlgciie3puigfe5bqjqqlgi2pphj.apps.googleusercontent.com')
            

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            data = {
                    "first_name": idinfo['given_name'],
                    "last_name": idinfo['family_name'],
                    "username": idinfo['name'],
                    "phone": None,
                    "email": idinfo['email'],
                    "password": idinfo['sub']
                    }
            if User.objects.filter(email=idinfo['email']).exists():
                r = requests.post(
                    'http://127.0.0.1:8000/api/token/obtain/',
                    headers={
                        'Content-Type': 'application/json',
                        'accept': 'application/json'
                    },
                    json=data
                )
                return Response(r.json())
            else:
                serializer = UserSerializer(data=data)
                if serializer.is_valid():
                    user = serializer.save()
                    if user:
                        r = requests.post(
                            'http://127.0.0.1:8000/api/token/obtain/',
                            headers={
                                'Content-Type': 'application/json',
                                'accept': 'application/json'
                            },
                            json=data
                        )
                        return Response(r.json(), status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as err:
            
            content = {'message': 'Invalid token'}
            return Response(content)



class UserCreate(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format='json'):
        if request.data['password'] != request.data['pswd'] :
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                if user:
                    json = serializer.data
                    return Response(json, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("password don't match", status=status.HTTP_400_BAD_REQUEST)




class postList(generics.ListCreateAPIView):
    serializer_class = PostSerializers
    queryset = Post.objects.all()

class postDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializers
    queryset = Post.objects.all()




class ImageList(generics.ListCreateAPIView):
    serializer_class = ImageSerializers

    def get_queryset(self):
        queryset = Image.objects.all()
        post = self.request.query_params.get('post')

        if post is not None:
            queryset = queryset.filter(post = post)

        return queryset

class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ImageSerializers

    queryset = Image.objects.all()



@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def WilayaList(request):
    if request.method == 'GET':
        Wilayas = Wilaya.objects.all()
        serializer = WilayaSerializers(Wilayas, many=True)
        return Response(serializer.data)

class WilayaDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WilayaSerializers
    queryset = Wilaya.objects.all()


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def CommuneList(request):
    if request.method == 'GET':
        Communes = Commune.objects.all()
        serializer = CommuneSerializers(Communes, many=True)
        return Response(serializer.data)

class CommuneDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommuneSerializers
    queryset = Commune.objects.all()

@api_view(['GET','POST'])
@permission_classes((permissions.AllowAny,))
def DiscussionList(request):
    if request.method == 'GET':
        Discussions = Discussion.objects.all()
        serializer = DiscussionSerializers(Discussions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DiscussionSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
@permission_classes((permissions.AllowAny,))
def MessageList(request):
    if request.method == 'GET':
        Messages = Message.objects.all()
        serializer = MessageSerializers(Messages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MessageSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)