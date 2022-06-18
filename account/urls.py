from django.urls import path
from . import views

urlpatterns = [
    path('verify-email/', views.email_verify, name='verify-email'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
]