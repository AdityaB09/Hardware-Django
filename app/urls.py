from django.urls import path
from . import views
# from django.conf import settings
# from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from  .forms import MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
urlpatterns = [
    path('',views.index, name = "index" ),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout, name='logout'),
    path('product/', views.product, name='product'),
    path('product/<slug:data>', views.product, name='productdata'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/' ), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html',form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),


]