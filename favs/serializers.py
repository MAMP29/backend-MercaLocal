from rest_framework import serializers
from .models import Favorito
from products.models import Producto, Categoria
from users.models import Cliente

class VendedorTiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre_tienda']

class CategoriaFavoritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

class ProductoFavoritoSerializer(serializers.ModelSerializer):
    vendedor = VendedorTiendaSerializer(read_only=True)
    categoria = CategoriaFavoritoSerializer(read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'stock', 'imagen', 'vendedor', 'categoria']

class FavoritoSerializer(serializers.ModelSerializer):
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(),
        source='producto',  # Mapea al campo 'producto' en el modelo
        write_only=True
    )
    producto = ProductoFavoritoSerializer(read_only=True) # Datos del producto (solo lectura)

    class Meta:
        model = Favorito
        fields = ['id', 'producto_id', 'producto', 'fecha_creacion']
        extra_kwargs = {
            'producto_id': {'required': True}, # Hace que el cliente sea obligatorio
            'producto': {'required': True}, # Hace que el producto sea obligatorio
        }

    def create(self, validated_data):
        cliente = self.context['request'].user
        producto = validated_data['producto']
        favorito, created = Favorito.objects.get_or_create(cliente=cliente, producto=producto)
        if not created:
            raise serializers.ValidationError("Este producto ya está en tus favoritos.")
        return favorito