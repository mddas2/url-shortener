# urls.py in url_shortener app
from django.urls import path
from .views import redirect_view,Dashboard

urlpatterns = [
    path('<str:short_key>/', redirect_view, name='redirect_view'),
    path('', Dashboard, name='user_dashboard'),

]
