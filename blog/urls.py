from . import views
from django.urls import path, include

search_urls_patterns=[
    path('', views.search, name='blog_search'),
    path('<int:id>', views.search, name="blog_search_page")
]


urlpatterns = [
    path('post/<int:id>/', views.Detail, name='blog_detail'),
    path('home/', views.home, name='blog_home'),
    path('home/<int:id>/', views.home, name='blog_home_page'),
    path('aboutme/', views.aboutme, name='blog_aboutme'),
    path('search/', include(search_urls_patterns))
]

