from django.urls import path
from . import views
from .views import *
# from django.conf import settings
# from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from  .forms import MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
urlpatterns = [
    path('',views.index, name = "index" ),

    path('token', token_send , name = "token"),
    path('success', success , name = "success"),
    path('verify/<auth_token>',verify, name = "verify"),
    path('error', error_page , name = "error"),


    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout, name='logout'),
    path('product/', views.product, name='product'),
    path('product/<slug:data>', views.product, name='productdata'),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    path('/buy-now/product-detail/<int:pk>/', views.ProductDetailBuyView.as_view(), name='product-detail-buy'),
    

    path('buy-now/', views.add_to_cart, name='add-to-cart'),  
    path('add-to-cart/', views.buynow, name='buynow'), 

    path('pluscart/',views.plus_cart, name='plus-cart'),   
    path('minuscart/', views.minus_cart, name='minus-cart'),
    path('removecart/', views.remove_cart, name='remove-cart'),
    path('cart/',views.show_cart, name='showcart'),
    # path('cart/emptycart/', views.empty_cart, name='emptycart'),
  
    path('search/', views.search, name='search'),
    path('contactus/', views.contactus, name='contactus'),
    path('aboutus/', views.aboutus, name='aboutus'),

    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),

    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/' ), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html',form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),


]