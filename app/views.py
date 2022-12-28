from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Product, Cart 
from itertools import chain
from django.core.paginator import Paginator
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
 

# Create your views here.
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user = user_object)
    return render(request, 'index.html', { 'user_profile': user_profile,})


def add_to_cart(request):
 user=request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()

 return redirect('/cart')

def empty_cart(request):
    return render(request, 'emptycart.html')


def show_cart(request) :
    if request.user.is_authenticated :
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
       
        if cart_product :
            for p in cart_product : 
                tempamount = (p.product.price * p.quantity)
                amount += tempamount
                totalamount = amount +shipping_amount
           
            return render(request, 'addtocart.html', {'carts': cart, 'totalamount' : totalamount, 'amount':amount, })
        else :
            return render (request,'emptycart.html')



def plus_cart(request):
    if request.method == 'GET' :
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      
        if cart_product :
            for p in cart_product : 
                tempamount = (p.product.price * p.quantity)
                amount += tempamount
                totalamount = amount +shipping_amount
                
            data = {
                'quantity' : c.quantity,
                'totalamount' : totalamount,
                'amount' : amount, 
                }
            return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET' :
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      
        if cart_product :
            for p in cart_product : 
                tempamount = (p.product.price * p.quantity)
                amount += tempamount
                totalamount = amount + shipping_amount
                
            data = {
                'quantity' : c.quantity,
                'totalamount' : totalamount,
                'amount' : amount, 
                }
            return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET' :
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        
        c.delete()

        
        
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        

    
        if cart_product == None :
            amount = 0.0
            shipping_amount = 00.0
            totalamount = 0.0
            print(len(cart_product))
        else :


    
         if cart_product :
            for p in cart_product : 
                tempamount = (p.product.price * p.quantity)
                amount += tempamount
                totalamount = amount + shipping_amount
                
        data = {
                'amount' : amount,
                'totalamount' : totalamount ,
                
                }
            
        return JsonResponse(data)


def product(request, data=None):
    if data == None:
     products = Product.objects.all().order_by('id')
     paginator = Paginator(products, 2)
     page_number = request.GET.get('page')
     page_obj = paginator.get_page(page_number)
    elif data == 'mobiles' :
        products = Product.objects.filter(category='M')
        paginator = Paginator(products, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    elif data == 'laptops' :
        products = Product.objects.filter(category='L')
        paginator = Paginator(products, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    elif data == 'processors' :
        products = Product.objects.filter(category='PR')
        paginator = Paginator(products, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    elif data == 'below' :
        products = Product.objects.filter(price__lt=250)
        paginator = Paginator(products, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    elif data == 'above' :
        products = Product.objects.filter(price__gt=250)
        paginator = Paginator(products, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, 'product.html',{'products' : page_obj})
    

def profile(request):
    user_profile=Profile.objects.get(user=request.user)
    #user_profile1 = User.objects.get(email=request.user.email)
    if request.method == 'POST' :
        if request.FILES.get('image') == None :
             image = user_profile.profileimg
             #bio = request.POST['bio']
             location = request.POST['location']
             
             first_name = request.POST['firstname']
             last_name = request.POST['lastname']
          #   birthdate = request.POST['birthdate']
             mobileno = request.POST['mobileno']
          #   email = user_profile1.email
             


             user_profile.profileimg = image
             #user_profile.bio = bio
             user_profile.location = location
             user_profile.first_name = first_name
             user_profile.last_name = last_name
         #    user_profile.birth_date = birthdate
             user_profile.mobile_no = mobileno
        #     user_profile1.email = email
             

             user_profile.save()
    if request.FILES.get('image') != None :
        image = request.FILES.get('image')
        #bio = request.POST['bio']
        location = request.POST['location']
                      
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        #birthdate = request.POST['birthdate']
        mobileno = request.POST['mobileno']
        #email = request.POST['email']


        user_profile.profileimg = image
        #user_profile.bio = bio
        user_profile.location = location

        user_profile.first_name = first_name
        user_profile.last_name = last_name
        # user_profile.birth_date = birthdate
        user_profile.mobile_no = mobileno
        #user_profile1.email = email
        
        user_profile.save()
        return redirect('profile')
   
    return render(request,'profile.html',{'user_profile':user_profile})

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()

                user_login = auth.authenticate(username=username, password=password1)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('profile')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render(request,'signup.html')

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

def logout(request):
    auth.logout(request)
    return redirect('signin')

class ProductDetailView(View) :
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'productdetail.html', {'product': product})