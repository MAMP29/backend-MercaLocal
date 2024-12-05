from django.urls import path
from . import views

urlpatterns = [
    path('crear-producto', views.create_producto, name='crear-producto'),
]