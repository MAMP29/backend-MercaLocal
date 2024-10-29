# Funciones para convertr objetos a JSON
from rest_framework import serializers
from .models import Cliente

# Clase para serializar el cliente, basado en el usuario por defecto de django
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'username', 'first_name', 'last_name','email', 'password', 'telefono', 'ciudad']
        extra_kwargs = {
            'password': {'write_only':True}  # Hace que la contraseña no se muestre en la respuesta
        }

    # Creación del cliente aquí mismo para evitar crearlo por fuera
    def create(self, validated_data):
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
        return cliente