from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'),
    path('<slug:cat_slug>/',sub_cat,name="sub_cat"),
]
