from django.urls import path
from . import views

urlpatterns = [
    path('crear-producto', views.create_producto, name='crear-producto'),
    path('listar-productos', views.list_productos, name='listar-productos'),
    path('<int:producto_id>', views.retrieve_producto, name='producto'),
    path('actualizar/<int:producto_id>', views.update_producto, name='actualizar-producto'),
    path('borrar/<int:producto_id>', views.delete_producto, name='eliminar-producto'),

    path('vendedor/<int:vendedor_id>/productos', views.list_productos_vendedor, name='listar-productos-vendedor'),
    path('vendedor/<int:vendedor_id>/producto/<int:producto_id>', views.retrieve_producto_vendedor, name='producto-vendedor'),

]