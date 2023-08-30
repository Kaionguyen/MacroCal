from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_page, name="home"),
    path("profile/<int:pk>/", views.profile, name="profile"),
    path("edit_profile/<int:pk>/", views.edit_profile, name="edit_profile"),
    path("metric/", views.metric, name="metric"),
    path("imperial/", views.imperial, name="imperial"),
    path("macrocal/", views.calculate_macros, name="macrocal"),
]
