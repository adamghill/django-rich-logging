from django.urls import path
from django.views.generic import TemplateView

from www import views


urlpatterns = [
    path("", views.index),
    path("error", views.error),
]
