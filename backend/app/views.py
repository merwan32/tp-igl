from django.shortcuts import render,redirect
from rest_framework import generics
from .models import *
from .serialezers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from google.oauth2 import id_token
from google.auth import transport
from urllib.parse import urlparse
import requests
from django.core.files.base import ContentFile
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim



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


@api_view(['POST'])
def CreatePost(request):
    adr = Adress()
    adr.lat = request.data['lat']
    adr.long = request.data['long']
    ad = geolocator.reverse(str(request.data['lat'])+","+str(request.data['long']))
    adr.commune = Commune.objects.filter(name__contains = str(ad.address)).first()
    adr.save()
    p = Post()
    p.user = request.user
    p.category = request.data['category']
    p.type = request.data['type']
    p.surface = request.data['surface']
    p.description = request.data['description']
    p.prix = request.data['prix']
    p.adress = adr
    p.save()
    for x in request.data['images']:
        i = Image()
        i.Post = p
        i.img = x
        i.save()
    return Response(request.data)


geolocator = Nominatim(user_agent="tpigl")
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def scrap(request):
    for i in range(1,10):
        try:
            r = requests.get("http://www.annonce-algerie.com/AnnoncesImmobilier.asp?rech_page_num="+str(i))
            soup = BeautifulSoup(r.content, features='lxml')
            articles = soup.findAll('tr',class_='Tableau1')  
            for a in articles:
                link = 'http://www.annonce-algerie.com/'
                x = a.findAll('td')
                link += x[7].find('a')['href']
                location = geolocator.geocode(x[1].text,timeout=None)
                try:
                    r2 = requests.get(link)
                    soup2 = BeautifulSoup(r2.content, features='lxml')
                    if soup2.findAll('td',class_='da_label_field')[3].text == 'Surface':
                        surface = soup2.findAll('td',class_='da_field_text')[3].text.replace(u' ',u'').replace(u'\xa0m²',u'')
                        description = soup2.findAll('td',class_='da_field_text')[5].text
                    elif soup2.findAll('td',class_='da_label_field')[2].text == 'Surface':
                        surface = soup2.findAll('td',class_='da_field_text')[2].text.replace(u' ',u'').replace(u'\xa0m²',u'')
                        description = soup2.findAll('td',class_='da_field_text')[4].text
                    else:
                        surface = 0
                        description = soup2.findAll('td',class_='da_field_text')[4].text

                    if not Post.objects.filter(description = description).count() and x[9].text.replace(' ','').replace(u'\xa0',u'') != 'n.d' and location and Commune.objects.filter(name__contains = str(x[1].text.strip())).first():
                        adr = Adress()
                        adr.lat = location.latitude
                        adr.long = location.longitude
                        adr.commune = Commune.objects.filter(name__contains = str(x[1].text.strip())).first()
                        adr.save()

                        p = Post()
                        p.user = User.objects.get(username = 'admin') 
                        p.category = x[3].text
                        p.type = x[5].text
                        p.prix = int(float(x[9].text.replace(' ','').replace(u'\xa0',u'')))
                        p.surface = surface
                        p.description = description
                        p.adress = adr
                        p.save()

                        imgs = soup2.findAll('table',class_='PhotoView1')
                        for img in imgs:
                            img_url = 'http://www.annonce-algerie.com/'+img.find('img')['src']
                            name = urlparse(img_url).path.split('/')[-1]

                            photo = Image() # set any other fields, but don't commit to DB (ie. don't save())

                            response = requests.get(img_url)
                            if response.status_code == 200:
                                photo.Post = p
                                photo.img.save(name, ContentFile(response.content), save=True)
                            
                    
                except Exception as e:
                    return Response('The scraping job failed. See exception 2: '+str(i)+str(e))

            
        except Exception as e:
            return Response('The scraping job failed. See exception: '+str(e))

    return redirect('../../app/post/')
        


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def adressList(request):
    p = Adress.objects.all()
    serializer = AdressSerializers(p, many=True)
    return Response(serializer.data)