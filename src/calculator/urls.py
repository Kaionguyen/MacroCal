from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing_page, name="home"),
    path("signup/", views.signup, name="signup"),
]
