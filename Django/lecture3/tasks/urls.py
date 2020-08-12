from django.urls import path
from . import views

app_name = "tasks" #This helps to uniquely identify urls with the same same
urlpatterns = [
    path("", views.index, name = "index"),
    path("add", views.add, name="add")
]
