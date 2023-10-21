from django.shortcuts import render
from products.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required()
def index(request):
    cat = Category.objects.all()
    context  = {'cats': cat}
    return render(request,'home/index.html',context)


@login_required()
def sub_cat(request,cat_slug):
    sub_cats = SubCategory.objects.filter(category__category_slug__iexact = cat_slug)
    context = {'sub_cats':sub_cats}
    return render(request,"home/sub_cats.html",context)