from django.urls import path
from .views import *


urlpatterns = [
    path('post/', postList.as_view()),
    path('post/<int:pk>/', postDetail.as_view()),
    path('image/', ImageList.as_view()),
    path('image/<int:pk>/', ImageDetail.as_view()),
    path('profile/', ProfileList.as_view()),
    path('profile/<int:pk>/', ProfileDetail.as_view()),
    path('wilaya/', WilayaList),
    path('wilaya/<int:pk>/', WilayaDetail.as_view()),
    path('commune/', CommuneList),
    path('commune/<int:pk>/', CommuneDetail.as_view()),
    path('discussion/', DiscussionList),
    path('message/', MessageList)
]