from django.urls import path
from .views import *

urlpatterns = [
    path('login/',user_login,name="user_login"),
    path('register/',user_register,name='user_register'),
    path('activate/<str:email_token>/',activate_email,name="activate_email"),
    path('add-to-cart/<uuid:product_uid>/',add_to_cart,name="add_to_cart"),
    path('cart/',cart,name="cart"),
    path('remove-cart-item/<uuid:cart_item_uuid>/',remove_cart_item,name="remove_cart_item"),
    path("remove-coupon/<uuid:cart_uuid>/",remove_coupon,name="remove_coupon"),
    path('success/',success,name="success"),
    path('logout/',user_logout,name="user_logout"),
]
