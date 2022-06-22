from django.urls import path
from . import views

urlpatterns = [
    path('verify-email/', views.email_verify, name='verify-email'),
    path('verify-email/<uidb64>/<token>', views.verification_email, name='verification-email'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register/first-step', views.register_first_step, name='register-first-step'),
    path('register/second-step', views.register_second_step, name='register-second-step'),
    path('', views.home, name='home'),
]