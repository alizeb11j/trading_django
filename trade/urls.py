from django.urls import path
from . import views


urlpatterns = [
    path("", views.test_ftn, name="trade-home"),
    path("data/", views.get_data, name="data")
]
