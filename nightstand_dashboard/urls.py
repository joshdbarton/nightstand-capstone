from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('registration/', views.register, name="registration"),
    path('login/', auth_views.LoginView.as_view(template_name="nightstand_dashboard/login.html"), name="login"),
    path("", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
]