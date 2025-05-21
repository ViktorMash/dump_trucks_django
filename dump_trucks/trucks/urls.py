from django.urls import path

from . import views


app_name = "trucks"

urlpatterns = [
    path("", views.truck_list, name="truck_list"),
]
