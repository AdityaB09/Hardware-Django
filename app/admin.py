from django.contrib import admin
from .models import Profile, Product, Cart, OrderPlaced, ContactUser
from django.utils.html import format_html
from django.urls import reverse


# Register your models here.
@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ["id","user", 
    "profileimg" ,
    'address' ,
    'locality' ,
    'city' ,
    'state' ,
    'pincode',
    'first_name', 
    'last_name', 
    'birth_date', 
    'mobile_no']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','price','description','category','product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','profile', 'profile_info','product', 'product_info','quantity','ordered_date','status']

    def profile_info(self,obj):
        link = reverse("admin:app_profile_change", args=[obj.profile.pk])
        return format_html('<a href="{}">{}</a>', link, obj.profile.first_name)

    def product_info(self,obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

@admin.register(ContactUser)
class ContactUserModelAdmin(admin.ModelAdmin):
    list_display = ["id","user", 
    'profile' ,
   # 'product' ,
    'email' ,
    'title' ,
    'description' , 
    'mobileno']