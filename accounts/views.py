from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from products.models import *
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
# Create your views here.

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.filter(username = email)
        if not user.exists():
            messages.add_message(request,messages.WARNING,"User not found.")
            return HttpResponseRedirect(request.path_info)
        
        if not user[0].profile.is_verified:
            messages.add_message(request,messages.WARNING,"User not verified.")
            return HttpResponseRedirect(request.path_info)
        
        user_obj = authenticate(username = email, password = password)
        if user_obj:
            login(request, user_obj)
            return redirect('/')
        messages.warning(request,"Invalid Credentials.")
        
    return render(request,"accounts/login.html")

def user_register(request):
    if request.method =="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.filter(username = email)
        if user.exists():
            messages.add_message(request,messages.WARNING,"User already exists.")
            return HttpResponseRedirect(request.path_info)
        
        #Here create_user automatically converts over password into hash.
        user_obj = User.objects.create_user(username=email,first_name = first_name, last_name = last_name,password=password, email = email)
        messages.add_message(request,messages.SUCCESS,"An email has been sent on your mail.")
        return HttpResponseRedirect(request.path_info)
        
    return render(request,"accounts/register.html")


def activate_email(request,email_token):
    try:
        user_profile = Profile.objects.get(email_token__iexact = email_token)
        user_profile.is_verified = True
        user_profile.save()
        return redirect('/')
    except Exception as e:
        print("activate_email...",e)
        
     
@login_required()   
def add_to_cart(request,product_uid):
    try:
        product = Product.objects.get(uuid = product_uid)
        user = request.user
        cart,_ = Cart.objects.get_or_create(user = request.user, is_paid = False)
        cart_item = CartItem.objects.create(cart = cart,product = product)
        
        if product.subcat.category.category_name == "Clothing":
            variant = request.GET.get('variant')
            if not variant:
                variant = 'L'
            size_variant = SizeVariant.objects.get(size_name = variant)
            cart_item.size_variant = size_variant
            cart_item.save()
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        return HttpResponse(e)
        print(e)
        

@login_required()
def remove_cart_item(request,cart_item_uuid):
    try:
        cart_item = CartItem.objects.get(uuid = cart_item_uuid)
        cart_item.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        print(e)


@login_required()
def cart(request):
    try:
        cart_manager = Cart.objects.get(is_paid = False, user = request.user)
        # print(cart_manager.cart_items.all().first().product.product_imagess.all().first().product_image.url)
        cart_items = CartItem.objects.filter(cart = cart_manager)
        # print(cart_items[0].product.product_imagess.all().first().product_image.url)
        # print(cart_items[0].cart.get_cart_total())
        if request.method == "POST":
            request.session['total'] = cart_manager.get_cart_total()
            coupon_code = request.POST.get('coupon_code')
            coupon_obj = Coupon.objects.filter(coupon_code__iexact = coupon_code)

            if not coupon_obj.exists():
                messages.add_message(request,messages.WARNING,"Invalid Coupon.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            if cart_manager.coupon == coupon_code:
                messages.add_message(request,messages.WARNING,"Coupon has already used.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            if cart_manager.get_cart_total() < coupon_obj[0].minimum_purchase_amount:
                messages.add_message(request,messages.WARNING,f"Amount should be greater then {coupon_obj[0].minimum_purchase_amount}.00")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            if coupon_obj[0].is_expired:
                messages.add_message(request,messages.WARNING,"Coupon has expired.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            cart_manager.coupon = coupon_obj[0]
            cart_manager.save()
            request.session['is_expired'] = True
            request.session['discount'] = coupon_obj[0].discount_price
            # print(cart_items[0].cart.get_cart_total())
            messages.add_message(request,messages.SUCCESS,"Coupon applied.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create({'amount':cart_manager.get_cart_total()*100,'currency':'INR','payment_capture':1}) #Yahaa * 100 isliye kiya kyoki razorpay amount paiso mein leta hai.
        # print("<-------------------------------------------------------------->")
        # print(payment)
        cart_manager.razorpay_order_id = payment['id']
        cart_manager.save()
        context  = {'cart_items':cart_items,'payment':payment}
        
        return render(request,"accounts/cart.html",context)
    except Exception as e:
        request.session['total'] = 0
        return render(request,"accounts/cart.html")
        # print(e)



@login_required()
def remove_coupon(request,cart_uuid):
    cart = Cart.objects.get(uuid = cart_uuid)
    cart.coupon = None
    cart.save()
    messages.add_message(request,messages.SUCCESS,"Coupon removed.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def success(request):
    order_id = request.GET.get('order_id')
    cart_manager = Cart.objects.get(razorpay_order_id = order_id)
    cart_manager.is_paid = True
    cart_manager.save()
    is_expired = request.session.get('is_expired',False)
    print(is_expired)
    if is_expired:
        print("I am in")
        cart_manager.coupon.is_expired = True
        cart_manager.coupon.save()
    request.session.flush()
    return HttpResponse("Payment Success.")

@login_required()
def user_logout(request):
    logout(request)
    return redirect('/accounts/login/')