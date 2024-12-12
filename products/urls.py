from django.urls import path
from . import views

urlpatterns = [
    path('crear-producto', views.create_producto, name='crear-producto'),
    path('listar-productos', views.list_productos, name='listar-productos'),
    path('<int:producto_id>', views.retrieve_producto, name='producto'),
    path('actualizar/<int:producto_id>', views.update_producto, name='actualizar-producto'),
    path('borrar/<int:producto_id>', views.delete_producto, name='eliminar-producto'),

    #path('categoria/<int:categoria_id>/listar', views.listar_productos_por_categoria, name='listar-productos-por-categoria'),

    path('buscar/', views.ProductoListView.as_view(), name='buscar-productos'),

    path('vendedor/<int:vendedor_id>/productos', views.list_productos_vendedor, name='listar-productos-vendedor'),
    path('vendedor/<int:vendedor_id>/producto/<int:producto_id>', views.retrieve_producto_vendedor, name='producto-vendedor'),

    # Endpoint para listar productos del vendedor
    path('mis-productos', views.list_mis_productos, name='mis-productos'),
]