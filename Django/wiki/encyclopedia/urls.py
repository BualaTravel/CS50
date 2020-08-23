from django.urls import path

from . import views
from .views import BlogListView

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("edit/<str:title>/", views.edit, name="edit"),
    path("<str:title>/", views.entry, name="entry"),
    path('', BlogListView.as_view(), name='blog_list'),



]
