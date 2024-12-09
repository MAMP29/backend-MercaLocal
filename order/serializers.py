from rest_framework import serializers
from .models import Pedido, DetallePedido, Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre', 'imagen']

class DetallePedidoSerializer(serializers.ModelSerializer):
    vendedor_nombre = serializers.SerializerMethodField()
    producto = ProductoSerializer()
    class Meta:
        model = DetallePedido
        fields = ['id', 'pedido', 'producto', 'cantidad', 'precio', 'vendedor_nombre']

    def get_vendedor_nombre(self, obj):
        return obj.producto.vendedor.nombre_tienda  # Calcula dinámicamente el nombre del vendedor

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
