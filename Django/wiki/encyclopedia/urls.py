from django.urls import path

from . import views
from .views import BlogListView

app_name = "encyclopedia"

urlpatterns = [
    path("wiki", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path('', BlogListView.as_view(), name='blog_list'),



]
