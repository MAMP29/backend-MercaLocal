from django.urls import path
from . import views

urlpatterns = [
    path('listar-carrito', views.listar_carrito, name='listar-carrito'),
    path('agregar-producto/<int:producto_id>', views.agregar_producto, name='agregar-producto'),
    path('actualizar-carrito', views.actualizar_carrito, name='actualizar-carrito'),
    path('eliminar-producto/<int:producto_id>', views.eliminar_producto, name='eliminar-producto'),
    path('vaciar-carrito', views.vaciar_carrito, name='vaciar-carrito'),
]