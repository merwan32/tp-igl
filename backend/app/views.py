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
from django.db.models import Q



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
                    "password": idinfo['sub'],
                    "profile_picture":idinfo['picture']
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

class detail(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PostSerializers
    def get_queryset(self):
        id = self.kwargs.get('postId')
        post = Post.objects.filter(Q(id = id))
        
        return  post
    
class detailimages(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ImageSerializers
    def get_queryset(self):
        id = self.kwargs.get('postId')
        images = Image.objects.filter(Q(Post_id = id))
            

        return  images
    
class mypostList(generics.ListAPIView):
    serializer_class = ImageSerializers
    def get_queryset(self):
        user = self.request.user
        posts = Post.objects.filter(Q(user=user))

        postid = []
        for p in posts:
            postid.append(p.id)
            

        images = Image.objects.filter(Q(Post__id__in=postid))
        seen_posts = set()
        new_list = []
        for obj in images:
            if obj.Post not in seen_posts:
                new_list.append(obj)
                seen_posts.add(obj.Post)  

        return  new_list

class myoffreList(generics.ListAPIView):
    serializer_class = OffreSerializers
    def get_queryset(self):
        user = self.request.user
        offres = Offre.objects.filter(Q(reciver=user))
            
        return  offres
    
class addoffre(generics.ListAPIView):
    serializer_class = OffreSerializers
    def post(self, request):
        user = self.request.user
        id = request.data['postId']
        post = Post.objects.get(id = id)

        offre = Offre()
        offre.sender = user
        offre.reciver = post.user
        offre.post = post
        offre.phone = request.data['phone']
        offre.prix = request.data['prix']
        offre.description = request.data['description']
        offre.save()
        
        return  Response(request.data)
    
@api_view(['POST'])
def CreatePost(request):
    adr = Adress()
    adr.lat = request.data['lat']
    adr.long = request.data['long']
    ad = geolocator.reverse(str(request.data['lat'])+","+str(request.data['long']), language="fr")
    print('err')
    print(ad.address.split(',')[-5].split()[0])
    adr.commune = Commune.objects.filter(name__contains = ad.address.split(',')[-5].split()[0]).first()
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
    images = request.FILES.getlist('images')
    for image in images:
        Image.objects.create(Post=p, img=image)
        
    return Response(request.data)

def DeletePost(request,id):
    
    Post.objects.get(id = id).delete()
    return Response(request)


class getcommunes(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CommuneSerializers
    def get_queryset(self):
        communes = Commune.objects.all()
        return  communes 



class getwilaya(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = WilayaSerializers
    def get_queryset(self):
        wilayas = Wilaya.objects.all() 
        return  wilayas


class SearchListAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ImageSerializers

    def get_queryset(self):
        query = self.request.GET.get('s')
        type = self.request.GET.get('type')
        wilaya = self.request.GET.get('wilaya')
        start_date = self.request.GET.get('first', None)
        end_date = self.request.GET.get('last', None)
        if start_date and end_date:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
        posts = Post.objects.filter(Q(description__contains=query) & Q(category__contains = type) & Q(adress__commune__wilaya__name__contains = wilaya)  ) if query else []
        
        postid = []
        for p in posts:
            postid.append(p.id)
            

        images = Image.objects.filter(Q(Post__id__in=postid))

        seen_posts = set()
        new_list = []
        for obj in images:
            if obj.Post not in seen_posts:
                new_list.append(obj)
                seen_posts.add(obj.Post) 

        return  images

class postsList(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ImageSerializers

    def get_queryset(self):
            

        images = Image.objects.all()

        seen_posts = set()
        new_list = []
        for obj in images:
            if obj.Post not in seen_posts:
                new_list.append(obj)
                seen_posts.add(obj.Post) 
            if len(new_list) == 16:
                break

        return  new_list

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