from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('registration/', views.register, name="registration"),
    path('login/', auth_views.LoginView.as_view(template_name="nightstand_dashboard/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add_book/", views.add_book, name="add_book"),
    path("books/<int:pk>", views.book_view, name="book_view")
]