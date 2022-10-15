from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('password-reset/done', views.password_reset_done,
         name='password_reset_done'),
    path('login/', views.auth_login, name='auth_login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('profile/',views.imgUpload, name='userprofile')
]
