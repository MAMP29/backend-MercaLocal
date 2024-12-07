from django.db import transaction
from rest_framework import serializers
from .models import Producto, Categoria, Cliente

# Clase para serializar el producto, basado en el modelo de django
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    vendedor = ClienteSerializer()
    categoria = CategoriaSerializer()
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'stock', 'descripcion', 'imagen',  'vendedor' ,'categoria']
        extra_kwargs = {
            'nombre': {'required': True}, # Hace que el nombre sea obligatorio
            'precio': {'required': True}, # Hace que el precio sea obligatorio
            'stock': {'required': True}, # Hace que el stock sea obligatorio
            'descripcion': {'required': True}, # Hace que la descripción sea obligatorio
            'imagen': {'required': True}, # Hace que la imagen sea obligatorio
            'vendedor': {'required': True}, # Hace que el cliente sea obligatorio
            'categoria': {'required': True}, # Hace que la categoria sea obligatorio
        }

    @transaction.atomic
    def create(self, validated_data):
        cliente = self.context['request'].user
        categoria = validated_data.pop('categoria')  # Obtenemos la instancia de categoría

        try:
            # Crear el producto directamente con todos los datos necesarios
            producto = Producto.objects.create(
                cliente=cliente,
                categoria=categoria,
                **validated_data
            )
        except Exception as e:
            raise serializers.ValidationError(f"Error al crear el producto: {str(e)}")

        return producto