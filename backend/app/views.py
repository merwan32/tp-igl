from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serialezers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions

# Create your views here.


class ObtainTokenPairWithinfoView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class UserCreate(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HelloWorldView(APIView):

    def get(self, request):
        return Response(data={"hello":"world"}, status=status.HTTP_200_OK)


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