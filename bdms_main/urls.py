"""bdms_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin 
from django.urls import path, include
#from django.conf import settings
#from django.conf.urls.static import static
#from bdmapp.common.views import HomeView, SignUpView, AboutView
from bdmapp.common.views import HomeView, SignUpView, AboutView, ProfileUpdateView, ProfileView, DonationView
from bdmapp.common import views
from bdmapp.common.views import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('donation/', DonationView.as_view(), name='donation'),
   # path('contact/',views.contact, name="contact"),
    #path('send-form-email/', views.SendFormEmail.as_view(), name='send_mail'),
    
    #path('donation/',views.doner),
    path('excel/', views.ExcelPageView.as_view(), name='excel'), 
    path('export/excel', views.export_users_xls, name='export_excel'),
    path('export/excel-styling', views.export_styling_xls, name='export_styling_excel'),
    path('export/export-write-xls', views.export_write_xls, name='export_write_xls'),
    
    path('contact/',views.ContactView.as_view(), name="contact"),

    path('profile-update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # Authentication 
    path('register/', SignUpView.as_view(), name="register"),

    path('login/', auth_views.LoginView.as_view(
        template_name='common/login.html'
        ),
        name='login'
    ),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'
        ),
        name='logout' 
    ),

    path(
        'change-password',
        auth_views.PasswordChangeView.as_view(
            template_name='common/change-password.html',
            success_url='/'
        ),
        name='change-password'
    ),

    
    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='common/password-reset/password_reset.html',
             subject_template_name='common/password-reset/password_reset_subject.txt',
             email_template_name='common/password-reset/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='common/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='common/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='common/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('oauth/', include('social_django.urls', namespace='social')),  # <-- here 

]#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)