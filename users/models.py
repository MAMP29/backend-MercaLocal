from pickle import FALSE

from django.contrib.auth.models import AbstractUser, Group, Permission, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Model


# Create your models here.

class Cliente(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name='Correo electrónico'
    )
    telefono = models.PositiveBigIntegerField(
        unique=False, blank=False, null=False,
        validators=[
            RegexValidator(
                regex=r'(3|6)\d{9}',
                message=('No es un número de teléfono válido'),
                code='invalid_phonenumber'
            )
        ],
        verbose_name='Número teléfono'
    )
    ciudad = models.CharField(
        max_length=100,
        verbose_name='Ciudad'
    )

    # Definiendo nombres de user original para evitar conflictos
    groups = models.ManyToManyField(
        Group,
        related_name="cliente_user_set",
        blank=True,
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="cliente_user_permissions",
        blank=True,
        verbose_name='user permissions'
    )

    # ATRIBUTOS EXCLUSIVOS PARA EL APARTADO DE VENDEDOR, ESTAN VACIOS DESDE UN PRINCIPIO,
    # AL SER VENDEDOR SE DEBEN PONER VALORES
    es_vendedor = models.BooleanField(default=False)
    nombre_tienda = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nombre de la tienda')

    USERNAME_FIELD = 'email' # Correo como autenticación principal en lugar de username
    REQUIRED_FIELDS = ['username', 'first_name','last_name','telefono', 'ciudad']

    class Meta:
        db_table = 'CLIENTE'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']
        #permissions = (
        #    ('can_buy_product', 'Can buy product'),
        #    ('can_sell_product', 'Can sell product'), # Tiene que ser un vendedor
        #)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.first_name = self.first_name.upper()
        self.last_name = self.last_name.upper()
        self.email = self.email.lower()
        super(Cliente, self).save()


class Vendedor(models.Model):
    # Quite el id, ya viene por defecto en los modelos de DJANGO
    nombre_tienda = models.CharField(
        max_length=100,
        verbose_name='Nombre de la tienda',
        unique=True
    )

    '''descripcion = models.TextField(
        max_length=500,
        default='Descripción de mi tienda'
    )'''


    #cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)