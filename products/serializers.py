from django.db import transaction
from rest_framework import serializers
from .models import Producto, Categoria, Cliente
from favs.models import Favorito

# Clase para serializar el producto, basado en el modelo de django
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['nombre_tienda']

class FavoritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorito
        fields = ['id']

# Serializador para obtener un producto
class ProductoSerializer(serializers.ModelSerializer):
    vendedor = ClienteSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    es_favorito = serializers.SerializerMethodField()
    
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'stock', 'descripcion', 'imagen', 'vendedor', 'categoria', 'es_favorito']
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
    def get_es_favorito(self, obj):
        request = self.context['request']
        #print('context ----- ', request)
        if request and hasattr(request.user, 'id'):  # Verificamos que el usuario tenga ID
            # Construimos la consulta de manera más explícita
            favorito_existe = Favorito.objects.filter(
                cliente_id=request.user.id,  # Accedemos al cliente a través de la relación con user
                producto_id=obj.id
            ).exists()
            return favorito_existe
        return False

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

# Serializador para crear un producto
class ProductoCreateSerializer(serializers.ModelSerializer):
    vendedor_nombre = serializers.SlugRelatedField(
        queryset=Cliente.objects.all(),
        slug_field='nombre_tienda',  # Campo que se utilizará para buscar al vendedor
        source='vendedor',  # Mapea al campo 'vendedor' en el modelo
        write_only=True
    )
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source='categoria',  # Mapea al campo categoría
        write_only=True
    )

    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'stock', 'descripcion', 'imagen', 'vendedor_nombre', 'categoria_id']

    @transaction.atomic
    def create(self, validated_data):
        try:
            producto = Producto.objects.create(**validated_data)
        except Exception as e:
            raise serializers.ValidationError(f"Error al crear el producto: {str(e)}")
        return producto