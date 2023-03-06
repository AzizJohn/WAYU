from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import small

urlpatterns = [
    path('sp/', small),
]
