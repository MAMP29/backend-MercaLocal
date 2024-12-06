from rest_framework import serializers
from .models import Pedido, DetallePedido


class DetallePedidoSerializer(serializers.ModelSerializer):
    vendedor_nombre = serializers.SerializerMethodField()

    class Meta:
        model = DetallePedido
        fields = ['id', 'pedido', 'producto', 'cantidad', 'precio', 'vendedor_nombre']

    def get_vendedor_nombre(self, obj):
        return obj.producto.vendedor.nombre_tienda  # Calcula dinámicamente el nombre del vendedor
