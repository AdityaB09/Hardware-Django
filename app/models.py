from django.db import models
from django.contrib.auth import get_user_model
from datetime import date


User = get_user_model()
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user =  models.IntegerField()
    profileimg = models.ImageField(upload_to='profile_images',default='about-comapny.jpg')
    location = models.CharField(max_length=101,blank=True)

    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    birth_date = models.DateField(default=date.today())
    mobile_no = models.IntegerField(default='9999999999')

    def __str__(self) :
        return self.user.username

CATEGORY_CHOICES = (
    ('M','Mobiles'),
    ('L','Laptops'),
    ('PR','Processors'),
)


class Product(models.Model) :
    title = models.CharField(max_length=100)
    price= models.FloatField()
    description = models.TextField()
    category = models.CharField(choices = CATEGORY_CHOICES, max_length=2)
    product_image =  models.ImageField(upload_to='productimg')

    def __str__(self):
        #return str(self.user)
        return str(self.id)