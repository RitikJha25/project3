"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views #import this
from django.contrib.auth.views import LogoutView
from users import views as user_view
from django.contrib.auth import views as auth
from payment.views import payment_success
urlpatterns=[
path('scripteditor',include('Meditor.urls')),
path('', include('mnfapp.urls')),
path('narration/', include('narration.urls')),
path('conversion/', include('conversion.urls')),
path('users/', include('users.urls')),
path('videos/', include('videos.urls')),
path('pay/', include('payment.urls')),
path('paytest/', include('testpay.urls')),
path('audit/', include('scriptAudit.urls')),

path('events/', include('events.urls')),
path('success/',payment_success,name="payment-success"),
path('admin/', admin.site.urls),
path('accounts/', include('allauth.urls')), 
path('myauth', TemplateView.as_view(template_name="users/fbLogin.html")),

path('logout', LogoutView.as_view()),
path('register/', user_view.register, name='register'),
path('activate/<uidb64>/<token>', user_view.activate, name='activate'),
path('social-auth/', include('social_django.urls', namespace="social")),
path('accounts/', include('allauth.urls')),
path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'), 
path("password_reset", auth_views.PasswordResetView.as_view(template_name = 'password/password_reset.html'), name="password_reset"),
path('verification/', include('verify_email.urls')),

path('register/', user_view.register, name ='register'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

