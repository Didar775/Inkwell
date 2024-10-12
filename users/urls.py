from django.urls import path
from . import views
from .views import user_list

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('', user_list, name='user_list'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
]