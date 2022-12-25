from django.contrib import admin
from .models import Profile, Product
# Register your models here.
admin.site.register(Profile)

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','price','description','category','product_image']