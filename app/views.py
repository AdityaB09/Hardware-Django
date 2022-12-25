from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Product 
from itertools import chain
 

# Create your views here.
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user = user_object)
    return render(request, 'index.html', { 'user_profile': user_profile,})


def product(request, data=None):
    if data == None:
     products = Product.objects.all()
    elif data == 'mobiles' :
        products = Product.objects.filter(category='M')
    elif data == 'laptops' :
        products = Product.objects.filter(category='L')
    elif data == 'processors' :
        products = Product.objects.filter(category='PR')
    elif data == 'below' :
        products = Product.objects.filter(price__lt=250)
    elif data == 'above' :
        products = Product.objects.filter(price__gt=250)
    return render(request, 'product.html',{'products' : products})
    

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