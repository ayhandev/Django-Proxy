from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('proxy/<path:target_url>/', views.proxy_view, name='proxy'),

]