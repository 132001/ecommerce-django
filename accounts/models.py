from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.email import send_account_activation_link
from django.contrib.sites.shortcuts import get_current_site
from products.models import *
# Create your models here.
class Profile(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    is_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length = 100)
    profile_image = models.ImageField(upload_to='profile_image/')
    
    
    def get_cart_count(self):
        return CartItem.objects.filter(cart__is_paid = False, cart__user = self.user).count() #Here we use CartItem because Cart is only one for one user so it will give us only 1 that not the correct answer.
    
class Cart(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="cart") #Ek cart ka ek hi cart rahega but hum yahaa Foreign key isliye kiye hai kyuki ek user multiple coupons rakh sakta hai jisase OneToOneField baadha abnta bich mien isiliye humne yahaa Foreignkey use kiya.
    coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=100,null=True,blank=True)
    razorpay_payment_id = models.CharField(max_length=100,null=True,blank=True)
    razorpay_payment_signature = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.user.username
    
    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = []
        for cart_item in cart_items:
            price.append(cart_item.product.price)
            if cart_item.color_variant:
                price.append(cart_item.color_variant.color_price)
            if cart_item.size_variant:
                price.append(cart_item.size_variant.size_price)
            
        if self.coupon:
            if self.coupon.minimum_purchase_amount < sum(price): #Yahaa par yeh isliye lagaya kyoki user pahale 2000 ki shopping cart mein add kar le uske baad woh coupon add kar le phir cart se item remove karta chalaa jaye toh ek time par humara cart ka amount humare minium_purchase_amount se bhi kam ho jayega aur woh uss par discount get kar lega so to prevent this we use this.
                return sum(price) - self.coupon.discount_price
        return sum(price)
    
    
class CartItem(BaseModel):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_items")
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True, related_name='product_cart_items')
    color_variant = models.ForeignKey(ColorVariant,on_delete=models.SET_NULL,null=True,blank=True)
    size_variant = models.ForeignKey(SizeVariant,on_delete=models.SET_NULL,null=True,blank=True)
    
    
    def get_product_price(self):
        price = [self.product.price]
        
        if self.color_variant:
            color_variant_price = self.color_variant.color_price
            price.append(color_variant_price)
        if self.size_variant:
            size_variant_price = self.size_variant.size_price
            price.append(size_variant_price)
        return sum(price)
            
        
    
    
@receiver(post_save,sender = User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
                email_token = str(uuid.uuid4().hex)
                email = instance.email
                site_url = "127.0.0.1:8000"
                if hasattr(instance, 'profile'):
                    profile = instance.profile
                    profile.email_token = email_token
                    profile.save()
                else:
                    profile = Profile(user=instance,email_token=email_token)
                    profile.save()
                send_account_activation_link(email, email_token, site_url)
    except Exception as e:
        print(e)
    
