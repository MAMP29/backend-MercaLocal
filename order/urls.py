from django.urls import path
from . import views

urlpatterns = [
    path('pedir-productos', views.checkout, name='pedir-productos'),
    path('obtener-detalle/<int:pedido_id>', views.obtener_detalle, name='obtener-detalle'),
    path('obtener-pedidos', views.obtener_pedido, name='obtener-pedidos'),
]