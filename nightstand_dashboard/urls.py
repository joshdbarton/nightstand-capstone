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
    path("books/<int:pk>", views.book_view, name="book_view"),
    path("book_add/<slug:olid>", views.book_add, name="book_add"),
    path("comment/<int:pk>", views.comment_view, name="add_comment"),
    path("like/<int:pk>", views.like, name="like"),
    path("complete/<int:pk>", views.complete_chapter, name="complete"),
    path("duedate/<int:pk>", views.duedate, name="duedate"),
    path("group_search/<slug:olid>", views.groups_view, name="groups"), 
    path("groups/<int:pk>", views.group_detail, name="group_detail"), 
    path("create_group/<slug:olid>", views.create_group, name="create_group"), 
    path("group_add/<int:pk>", views.group_add, name="group_add"),
    path("delete_user_book/<int:pk>", views.delete_user_book, name="delete_user_book"),
    path("leave_group/<int:pk>", views.leave_group, name="leave-group"),
]