from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing_page, name="home"),
    path("macrocal/", views.macro_cal, name="macrocal"),
    path("signup/", views.user_signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
]
