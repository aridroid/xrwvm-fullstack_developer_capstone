# server/djangoapp/urls.py
from django.urls import path
from . import views

app_name = 'djangoapp'   # important — enables "djangoapp:about" reverse

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('dealers/', views.get_dealerships, name='dealers'),
    path('dealers/<int:dealer_id>/', views.dealer_detail, name='dealer-detail'),
    path('dealers/<int:dealer_id>/review/', views.review_dealer, name='dealer-review'),

    # auth pages
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_page, name='logout'),

    # API endpoints (if you need them)
    path('api/dealers/', views.api_get_dealers, name='api-dealers'),
    path('api/login/', views.login_user, name='api-login'),
    path('api/logout/', views.api_logout, name='api-logout'),
]
