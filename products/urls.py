from django.urls import path
from .views import *

urlpatterns = [
    path('<slug:subcat_slug>/',get_products,name="get_product"),
    path("item/<slug:item_slug>/",item,name="item"),
]
