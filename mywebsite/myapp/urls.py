from django.urls import path

from .views import *

urlpatterns = [
    #localhost:8000/
    path('', home, name="home-page"),
    #localhost:8000/about
    path('about/', aboutUs, name="about-page"),
    path('contact/', contact, name="contact-page"),
    path('showcontact/', showContact, name="showcontact-page"),
    path('register/', userRegist, name="register-page"),
    path('profile/', userProfile, name="profile-page"),
    path('editprofile/', editProfile, name="editprofile-page"),
]
