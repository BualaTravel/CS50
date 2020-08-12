from django.urls import path
from . import views     # . is the local directory

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.greet, name="greet"),
    path("crystian", views.crystian, name="crystian")
]
