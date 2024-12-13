import  django_filters
from .models import Producto

class ProductFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(field_name='nombre', lookup_expr='icontains')  # Filtrar por nombre (contiene)
    precio_min = django_filters.NumberFilter(field_name='precio', lookup_expr='gte')  # Filtrar por precio (mínimo y máximo)
    precio_max = django_filters.NumberFilter(field_name='precio', lookup_expr='lte')
    categoria = django_filters.NumberFilter(field_name='categoria__id')  # Cambiado para filtrar por ID de categoría


    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'categoria']