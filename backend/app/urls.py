from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('post/', postList.as_view()),
    path('post/<int:pk>/', postDetail.as_view()),
    path('image/', ImageList.as_view()),
    path('image/<int:pk>/', ImageDetail.as_view()),
    path('wilaya/', WilayaList),
    path('wilaya/<int:pk>/', WilayaDetail.as_view()),
    path('commune/', CommuneList),
    path('commune/<int:pk>/', CommuneDetail.as_view()),
    path('discussion/', DiscussionList),
    path('message/', MessageList),
    path('user/create/', UserCreate.as_view(), name="create_user"),
    path('token/obtain/',  jwt_views.TokenObtainPairView.as_view(), name='token_create'), 
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('google-login/', GoogleView.as_view(), name='google-login'),

]