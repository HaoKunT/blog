from . import views
from django.urls import path, include

search_urls_patterns=[
    path('', views.search, name='blog_search'),
    path('<int:id>', views.search, name="blog_search_page")
]

sign_urls_patterns = [
    path('signin', views.signinhtml, name="blog_signin"),
    path('signup', views.signuphtml, name="blog_signup"),
    path('signinfun', views.signin, name="blog_signinfun"),
    path('signupfun', views.signup, name="blog_signupfun"),
    path('logout', views.logout_view, name="blog_logout")
]

urlpatterns = [
    path('post/<int:id>/', views.Detail, name='blog_detail'),
    path('home/', views.home, name='blog_home'),
    path('home/<int:id>/', views.home, name='blog_home_page'),
    path('aboutme/', views.aboutme, name='blog_aboutme'),
    path('search/', include(search_urls_patterns)),
    path('sign/', include(sign_urls_patterns))
]

