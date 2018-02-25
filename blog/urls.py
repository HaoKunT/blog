from . import views
from django.urls import path

urlpatterns = [
    path('post/<int:id>/', views.Detail, name='blog_detail'),
    path('home/', views.home, name='blog_home'),
    path('home/<int:id>/', views.home, name='blog_home_page'),
]