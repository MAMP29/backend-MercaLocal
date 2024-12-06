from django.db import models
from users.models import Cliente
from products.models import Producto

# Create your models here.
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total')
    estado = models.CharField(
        max_length=20,
        choices=[('pendiente', 'Pendiente'), ('confirmado', 'Confirmado'), ('enviado', 'Enviado'), ('entregado', 'Entregado')],
        default='pendiente'
    )

    class Meta:
        db_table = 'PEDIDO'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['id']

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, verbose_name='Pedido')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad')
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')

    class Meta:
        db_table = 'DETALLE_PEDIDO'
        verbose_name = 'Detalle pedido'
        verbose_name_plural = 'Detalles pedidos'
        ordering = ['id']

