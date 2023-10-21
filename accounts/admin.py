from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('is_verified','email_token','profile_image','user')
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user','is_paid','coupon']
    
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart','product','size_variant','color_variant']