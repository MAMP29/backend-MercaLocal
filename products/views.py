from rest_framework.decorators import api_view
from users.permission import EsVendedor
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from products.serializers import ProductoSerializer
# Create your views here.


# Función para crear un producto solo si es un vendedor

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([EsVendedor])
def create_producto(request):
    serializer = ProductoSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        serializer.save()
        return Response({
            "nombre": serializer.data['nombre'],
            "message": "Producto creado con éxito"
        }, status=status.HTTP_201_CREATED)

    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


