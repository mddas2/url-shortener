# urls.py in url_shortener app
from django.urls import path
from .views import redirect_view,Dashboard,create_url,delete_url

urlpatterns = [
    path('<str:short_key>/', redirect_view, name='redirect_view'),
    path('', Dashboard, name='user_dashboard'),
    path('generate-url', create_url, name='create_url'),
    path('generate-url/<int:item_id>/', create_url, name='create_or_update_url_with_id'),
    path('delete-url/<int:id>', delete_url, name='delete_url'),
    # path('detail-url<int:id>', detailUrl, name='create_url'),

]
