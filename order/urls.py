from django.urls import path
from . import views

urlpatterns = [
    path('pedir-productos', views.checkout, name='pedir-productos'),
    path('obtener-pedido/<int:pedido_id>', views.obtener_pedido, name='obtener-pedido'),
]