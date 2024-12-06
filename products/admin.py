from django.contrib import admin
from .models import Producto, Categoria

# Registro del modelo Producto
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'stock', 'fecha_publication', 'categoria', 'vendedor')  # Qué campos mostrar en el listado
    search_fields = ('nombre', 'categoria__nombre')  # Campos por los que puedes buscar
    list_filter = ('categoria', 'vendedor')  # Filtros para la barra lateral
    list_per_page = 20  # Cuántos productos mostrar por página en el admin

# Registro del modelo Categoria
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')  # Qué campos mostrar en el listado
    search_fields = ('nombre',)  # Campos por los que puedes buscar

# Registrar los modelos y sus administradores personalizados
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
