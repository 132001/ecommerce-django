from django.contrib import admin
from .models import *
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name','cat_image','category_slug']
    
    def cat_image(self,obj):
        return format_html(f"<img src={obj.category_image.url} style='width:100px'/>")

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['subcat_name','sub_cat_image','subcat_slug','category']
    
    def sub_cat_image(self,obj):
        return format_html(f"<img src={obj.subcat_image.url} style='width:100px'/>")
    

@admin.register(ColorVariant)
class ColorVariantModel(admin.ModelAdmin):
    list_display=['color_name', 'color_price']
    

@admin.register(SizeVariant)
class SizeVariantModel(admin.ModelAdmin):
    list_display = ['size_name','size_price']

class ProductImageAdmin(admin.StackedInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
     inlines = [ProductImageAdmin]
     list_display = ['product_name','price','product_description','product_slug','subcat']

admin.site.register(Product,ProductAdmin)

@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ['product','show_image']
    
    def show_image(self,obj):
        return format_html(f"<img src={obj.product_image.url} style='width:100px'/>")
    

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['coupon_code','is_expired','discount_price','minimum_purchase_amount']