from django.db import models
from users.models import Cliente

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nombre')

    class Meta:
        db_table = 'CATEGORIA'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.nombre = self.nombre.upper()
        super(Categoria, self).save()

        
class Producto(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nombre')
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, verbose_name='Precio')
    stock = models.PositiveIntegerField(default=0, verbose_name='Stock')
    descripcion = models.TextField(blank=False, null=False, verbose_name='Descripción')
    fecha_publication = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de publicación')
    imagen = models.ImageField(upload_to='imagenes/productos/', blank=False, null=False, verbose_name='Imagen')
    vendedor = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Vendedor')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoria')

    class Meta:
        db_table = 'PRODUCTO'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']

