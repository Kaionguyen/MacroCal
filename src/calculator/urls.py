from django.urls import path

from . import views

urlpatterns = [
    path("", views.nutrition_data, name="nutrition_data"),
]
