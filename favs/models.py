from django.db import models
from users.models import Cliente
from products.models import Producto

# Create your models here.

class Favorito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        db_table = 'FAVORITO'
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
        unique_together = ('cliente', 'producto')
        ordering = ['id']

    def str(self):
        return f"{self.cliente.email} - {self.producto.nombre}"