from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
from ckeditor.fields import RichTextField
# Create your models here.


class Category(BaseModel):
    category_name = models.CharField(max_length = 100)
    category_image = models.ImageField(upload_to='category_images/')
    category_slug = models.SlugField(unique=True, null= True,blank=True)
    
    def save(self,*args,**kwargs):
        self.category_slug = slugify(self.category_name)
        super(Category, self).save(*args,**kwargs) 
        
    def __str__(self):
        return self.category_name
    
class SubCategory(BaseModel):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="sub_category")
    subcat_name = models.CharField(max_length=256)
    subcat_image = models.ImageField(upload_to="subcategory_images/")
    subcat_slug = models.SlugField(unique=True,null=True,blank=True)
    
    def save(self,*args,**kwargs):
        self.subcat_slug = slugify(self.subcat_name)
        super(SubCategory,self).save(*args,**kwargs)
        
    def __str__(self):
        return self.subcat_name

class ColorVariant(BaseModel):
    color_name = models.CharField(max_length = 100)
    color_price = models.IntegerField(default=0)
    
    def __str__(self):
        return self.color_name

class SizeVariant(BaseModel):
    size_name = models.CharField(max_length = 100)
    size_price = models.IntegerField(default=0)
    
    def __str__(self):
        return self.size_name

class Product(BaseModel):
    product_name = models.CharField(max_length = 100)
    subcat = models.ForeignKey(SubCategory,on_delete=models.CASCADE, related_name = "products")
    price = models.IntegerField()
    product_description = RichTextField()
    product_slug = models.SlugField(unique=True, null= True, blank=True)
    color_variant = models.ManyToManyField(ColorVariant,blank=True) #Beacuse many products many colors mein available ho sakate hai at the same time like choice field.
    size_variant = models.ManyToManyField(SizeVariant,blank=True)
    
    def save(self,*args,**kwargs):
        self.product_slug = slugify(self.product_name)
        super(Product,self).save(*args,**kwargs)
        
    def __str__(self):
        return self.product_name
    
    
    def get_product_price_by_size(self,size):
        return self.price + SizeVariant.objects.get(size_name = size).size_price
        
    
class ProductImages(BaseModel):
    product_image = models.ImageField(upload_to = "product_images/")
    product = models.ForeignKey(Product,on_delete = models.CASCADE,related_name = "product_imagess")
    
    
class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=20)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_purchase_amount = models.IntegerField(default=300)

    def __str__(self):
        return self.coupon_code