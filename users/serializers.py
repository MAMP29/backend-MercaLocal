# Funciones para convertr objetos a JSON
from rest_framework import serializers
from .models import Cliente

# Clase para serializar el cliente, basado en el usuario por defecto de django
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'username', 'first_name', 'last_name','email', 'password', 'telefono', 'ciudad']
        extra_kwargs = {
            'password': {'write_only':True},  # Hace que la contraseña no se muestre en la respuesta
            'email': {'required': True} # Hace que el email sea obligatorio
        }

    # Creación del cliente aquí mismo para evitar crearlo por fuera
    def create(self, validated_data):
        password = validated_data.pop('password')
        cliente = Cliente.objects.create_user(**validated_data)
        cliente.set_password(password)
        cliente.save()
        return cliente

    '''def create(self, validated_data):
        cliente = Cliente(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            telefono=validated_data['telefono'],
            ciudad=validated_data['ciudad'],
        )
        # Hashea la contraseña antes de guardarla
        cliente.set_password(validated_data['password'])
        cliente.save()
        return cliente'''

'''
# Serielizador para el venedor, solo tiene que guardar/solicitar los atributos relacionados a un cliente
class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['is_vendedor', 'nombre_tienda']
        extra_kwargs = {
            'is_vendedor': {'write_only':True},
            'nombre_tienda': {'write_only':True}
        }
'''

# Clase para convertir un cliente en un vendedor
class ConvertirVendedorSerializer(serializers.ModelSerializer):
    nombre_tienda = serializers.CharField(source='cliente.nombre_tienda')

    class Meta:
        model = Cliente
        fields = ['nombre_tienda']

    # Valida que no este vacio en nombre de la tienda
    def validate_nombre_tienda(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError('El nombre de la tienda no puede estar vacio')
        return value

    # Actualiza el cliente con el nuevo valor de nombre de la tienda
    def update(self, instance, validated_data):
        instance.nombre_tienda = validated_data['nombre_tienda']
        instance.save()
        return instance
