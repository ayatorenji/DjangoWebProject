from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

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
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('cart/', cart_review, name='cart-review'),
    path('admin-carts/', admin_cart_review, name='admin-cart-review'),
    path('update-cart/', update_cart, name='update-cart'),
    path('update-cart-status/<int:cart_id>/', update_cart_status, name='update-cart-status'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)