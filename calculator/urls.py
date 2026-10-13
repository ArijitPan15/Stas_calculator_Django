from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("standard-deviation/", views.standard_deviation_view, name="standard_deviation"),
    path("iqr/", views.iqr_view, name="iqr"),
]
