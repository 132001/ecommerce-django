from django.shortcuts import render
from .models import *
from accounts.models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required()
def get_products(request,subcat_slug):
    products = Product.objects.filter(subcat__subcat_slug__iexact = subcat_slug)
    context = {"products":products}
    return render(request,'products/all_products.html',context)


@login_required()
def item(request,item_slug):
    try:
        product = Product.objects.get(product_slug__iexact = item_slug)
        # images = product[0].product_imagess.all() We can do the same thing into html file.
        context = {'product':product}
        if request.GET.get('size'):
            size = request.GET.get('size')
            print(size)
            price = product.get_product_price_by_size(size)
            print(price,"Price")
            context['updated_size'] = size
            context['updated_price'] = price
        return render(request,"products/product.html",context)
    except Exception as e:
        print(e)
        
