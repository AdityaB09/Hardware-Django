from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth, AnonymousUser
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Product, Cart, OrderPlaced, ContactUser
from itertools import chain
from django.core.paginator import Paginator
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
import uuid
 

# Create your views here.
def index(request):
    try:
     user_object = User.objects.get(username=request.user.username)
     user_profile = Profile.objects.get(user = user_object)
    except User.DoesNotExist:
     user_profile = AnonymousUser()
    # user_object = User.objects.get(username=request.user.username)
    # user_profile = Profile.objects.get(user = user_object)
    return render(request, 'index.html', { 'user_profile': user_profile,})

def aboutus(request):
    return render(request, 'aboutus.html')

def contactus(request):
    user = request.user
    email = request.user.email
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)
    mobileno = user_profile.mobile_no
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        query = request.POST['query']
        
        ContactUser(user=user, email=email, profile=user_profile, query=query, mobileno = mobileno, title=title, description=description).save()
        
    else :
        render(request, 'contactus.html')
    return render(request, 'contactus.html',{'user_profile':user_profile, "user_object" :user_object })


def search(request):   
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)
    # email = request.user.email
    print(user_profile.mobile_no)
    #print(user_profile.last_name)
    print(user_object.email)
    query = request.GET['title']
        
    if len(query) > 51 :
            queryAll = Product.objects.none()
    else :
            allTitle = Product.objects.filter(title__icontains=query)
            allDesc = Product.objects.filter(description__icontains=query)
            #allManual = Product.objects.filter(manual__icontains=query)
            queryAll = allTitle | allDesc # | allManual 
    if queryAll.count() == 0:
            messages.warning(request, "No product found")
            
    return render(request, 'search.html', {'user_profile' : user_profile, "queryAll" : queryAll, "query": query,})


#@login_required
def address(request):
 add = Profile.objects.filter(user=request.user)
 user_object = User.objects.get(username=request.user.username)
 user_profile = Profile.objects.get(user = user_object)
 totalitem = 0
 if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'address.html', {'add':add, 'totalitem':totalitem, 'user_profile':user_profile,})

#@login_required
def orders(request):  
     totalitem = 0
     op = OrderPlaced.objects.filter(user=request.user)
     if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
      print(op)
     return render(request, 'orders.html', {'order_placed':op, 'totalitem':totalitem,})


def checkout(request):
    user= request.user
    add = Profile.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 10.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]

    if cart_product :
            for p in cart_product : 
                tempamount = (p.product.price * p.quantity)
                amount += tempamount
            totalamount = amount +shipping_amount
    return render(request, 'checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items})


def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    profile = Profile.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart :
        OrderPlaced(user=user, profile=profile, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')


def add_to_cart(request):
 user=request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()

 return redirect('/cart')

def empty_cart(request):
    return render(request, 'emptycart.html')

def buynow( request,**kwargs):
    template_name = "productdetail.html"
    user=request.user
    # product = Product.objects.get(pk=pk)
        # return render(request, 'productdetail.html', {'product': product})
    prod_id = request.GET.get('prod_id')
    product = Product.objects.get(id=prod_id)
    Cart(user=user, product=product).save()
    return render(request, template_name, {'product': product})

def show_cart(request) :
    if request.user.is_authenticated :
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 10.0
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
        shipping_amount = 10.0
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
        shipping_amount = 10.0
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

        cart = Cart.objects.filter(user=request.user)
        
        amount = 0.0
        shipping_amount = 10.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        
   #\/ Not in Project
   #\/ 
   #\/
   #\/
   #\/
   #\/
    
        if cart_product == None :
            amount = 0.0
            shipping_amount = 00.0
            totalamount = 0.0
            return render(request, 'addtocart.html', {'carts': cart , 'totalamount' : totalamount, 'amount':amount, })
        else :

 #/\ Not in Project
 #/\
 #/\
 #/\
 #/\
 #/\
    
         if cart_product :
            for p in cart_product : 
                tempamount = (p.product.price * p.quantity)
                amount += tempamount
                totalamount = amount + shipping_amount
                
        #     return render(request, 'addtocart.html', {'carts': cart , 'totalamount' : totalamount, 'amount':amount, })
        #     #return render(request, 'addtocart.html', {'carts': cart , 'totalamount' : totalamount, 'amount':amount, })
        #  else :
        #     return render(request,'emptycart.html')
               # return render(request, 'addtocart.html', {'carts': cart , 'totalamount' : totalamount, 'amount':amount, })
         data = {
                'amount' : amount,
                'totalamount' : totalamount ,
                
                }
         
         return JsonResponse(data)
        return render(request, 'addtocart.html', {'carts': cart , 'totalamount' : totalamount, 'amount':amount, })
        


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
            #  if request.POST.get('birthdate1') == None :
            #     birthdate1 =  
             address = request.POST.get('address')
             city = request.POST.get('city')
             state = request.POST.get('state')
             pincode = request.POST.get('pincode')
             image = user_profile.profileimg
             #bio = request.POST['bio']
             locality = request.POST['locality']
             
             first_name = request.POST['firstname']
             last_name = request.POST['lastname']
             birthdate = request.POST['birthdate']
             mobileno = request.POST['mobileno']
          #   email = user_profile1.email
             

             user_profile.address = address
             user_profile.city = city
             user_profile.state = state
             user_profile.pincode = pincode
             user_profile.locality = locality


             user_profile.profileimg = image
             #user_profile.bio = bio
             #user_profile.city = city
             user_profile.first_name = first_name
             user_profile.last_name = last_name
             user_profile.birth_date = birthdate
             user_profile.mobile_no = mobileno
             #user_profile1.email = email
             

             user_profile.save()
             return redirect('/')
    if request.FILES.get('image') != None :
        image = request.FILES.get('image')
        #bio = request.POST['bio']
        locality = request.POST['locality']

        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        birthdate = request.POST['birthdate']
        mobileno = request.POST['mobileno']
        #email = request.POST['email']
 
        user_profile.address = address
        user_profile.city = city
        user_profile.state = state
        user_profile.pincode = pincode
        user_profile.locality = locality

        user_profile.profileimg = image
        #user_profile.bio = bio
        user_profile.city = city

        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.birth_date = birthdate
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
        try:
         if username == '' :
            # messages.success(request, "We've sent you an Email Please Check your Email Address")
             messages.warning(request,"No Username provided")
             return redirect('signup')
         if email == "" :
            messages.warning(request,"No Email Address provided")
            return redirect('signup')

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

                # user_login = auth.authenticate(username=username, password=password1)
                # auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                auth_token = str(uuid.uuid4())
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id, auth_token= auth_token) 
                new_profile.save()
                sendmail(email, auth_token)
                messages.success(request, "We've sent you an Email to verify your Email Address")
                return redirect('signup')
        
         else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        except Exception as e:
            print(e)
    else:
        return render(request,'signup.html')


def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # profile_obj = Profile.objects.filter(user=user)
        user_obj = User.objects.filter(username=username).first()
        user = auth.authenticate(username=username, password=password)
        profile_obj = Profile.objects.filter(user=user_obj).first()
        #print(profile_obj.is_verified)
        if not profile_obj :
         messages.info(request, 'Profile is not verified')
         return redirect('signin')   

        if profile_obj.is_verified :
          if user is not None:
            auth.login(request, user)
            return redirect('/')
          else:
            messages.info(request, 'User Not Found')
            return redirect('signin')
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
        print(pk)
        return render(request, 'productdetail.html', {'product': product})

class ProductDetailBuyView(View) :
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'productdetail.html', {'product': product})

def success(request):
    return render(request,'success.html')

def token_send(request):
    return render(request,'token_send.html')

def sendmail(email,token):
    subject = 'Your account has been verified.'
    message = f'Hi Paste the link to verify your account http://127.0.0.1:8000/verify/{token}' 
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def verify(request, auth_token):
    try :
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        
        if profile_obj:
            
            if profile_obj.is_verified:
                messages.success(request, 'Your Account is Already Verified')
                return redirect('signin')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Profile updated and Verified')
            return redirect('signin')
        else :
            messages.error(request, 'Authentication Error')
            
            return redirect('/error')
    except Exception as e :
        print(e)
        return redirect('signin')

def error_page(request):
    return render(request, 'error.html')
        

