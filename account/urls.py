from django.contrib import admin
from django.urls import path

from . import views

app_name='account'
urlpatterns = [
    path('login',views.login_user,name='login_user'),
    path('signup',views.signup,name='signup'),
    path('logout',views.logout_user,name='logout_user'),
]