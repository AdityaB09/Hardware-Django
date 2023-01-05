from django.db import models
from django.contrib.auth import get_user_model
from datetime import date


User = get_user_model()
# Create your models here.


STATE_CHOICES = (
('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
('Andhra Pradesh', 'Andhra Pradesh'),
('Arunachal Pradesh','Arunachal Pradesh'),
('Assam','Assam'),
('Bihar','Bihar'),
('Chandigarh','Chandigarh'),
('Chattisgarh','Chattisgarh'),
('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
('Daman & Diu','Daman & Diu'),
('Delhi','Delhi'),
('Goa','Goa'),
('Gujarat','Gujarat'),
('Haryana','Haryana'),
('Himachal Pradesh','Himachal Pradesh'),
('Jammu & Kashmir','Jammu & Kashmir'),
('Karnataka','Karnataka'),
('Kerala','Kerala'),
('Lakshwadeep','Lakshwadeep'),
('Madhya Pradesh','Madhya Pradesh'),
('Maharashtra','Maharashtra'),
('Manipur','Manipur'),
('Meghalaya','Meghalaya'),
('Mizoram','Mizoram'),
('Nagaland','Nagaland'),
('Odisha','Odisha'),
('Puducherry','Puducherry'),
('Punjab','Punjab'),
('Rajasthan','Rajasthan'),
('Sikkim','Sikkim'),
('Tamil Nadu','Tamil Nadu'),
('Telangana','Telangana'),
('Tripura','Tripura'),
('Uttarakhand','Uttarakhand'),
('Uttar Pradesh','Uttar Pradesh'),
('West Bengal','West Bengal'),
)

class Profile(models.Model):


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profileimg = models.ImageField(upload_to='profile_images',default='about-comapny.jpg')
    id_user =  models.IntegerField()
    address = models.CharField(max_length=1000, blank=True)
    locality = models.CharField(max_length=101,blank=True)
    city = models.CharField(max_length=101,blank=True)
    state = models.CharField(choices = STATE_CHOICES, max_length=55)
    pincode = models.IntegerField(default=400600)

    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)

    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    birth_date = models.DateField(default=date.today())
    mobile_no = models.IntegerField(default='9999999999')

    def __str__(self) :
        return (self.first_name)

CATEGORY_CHOICES = (
    ('M','Mobiles'),
    ('L','Laptops'),
    ('PR','Processors'),
)


class Product(models.Model) :
    title = models.CharField(max_length=100)
    price= models.FloatField()
    description = models.TextField()
    category = models.CharField(choices = CATEGORY_CHOICES, max_length=200)
    product_image =  models.ImageField(upload_to='productimg')

    def __str__(self):
        #return str(self.user)
        return str(self.title)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product =  models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    # def __str__(self) :
    #  return str(self.)

    @property
    def total_cost(self):
      return ( self.quantity * self.product.price)

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed', 'Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)

class OrderPlaced(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    # def __str__(self):
    #     return str(self.id)
    @property
    def total_cost(self):
      return ( self.quantity * self.product.price)

HELP_CHOICES = (
    ('Mobile','Mobile'),
    ('Laptop','Laptop'),
    ('Processor','Processor'),
    ('Others','Others'),

)

class ContactUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    #product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    query = models.CharField(choices = HELP_CHOICES, max_length=200)
    mobileno = models.IntegerField()
    email = models.EmailField()
    title = models.CharField(max_length= 100)
    description = models.CharField(max_length=2000)

    # def __str__(self):
    #     return str(self.id)

