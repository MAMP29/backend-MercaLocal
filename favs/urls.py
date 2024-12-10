from django.urls import path
from . import views

urlpatterns = [
    path('listar', views.listar_favoritos, name='listar-favoritos'),
    path('borrar/<int:pk>', views.delete_favorito, name='eliminar-favorito'),
    path('anadir', views.add_favorito, name='agregar-favorito'),
]