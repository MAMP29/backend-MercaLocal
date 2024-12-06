from rest_framework.decorators import api_view
from users.permission import EsVendedor
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from products.serializers import ProductoSerializer
from .models import Producto
from users.models import Cliente
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

# Función para listar todos los productos del usuario que es vendedor
# Revisar si se puede eliminar el campo del vendedor al devolver la lista de productos, pues es redundante
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([EsVendedor])
def list_productos(request):
    productos = Producto.objects.filter(cliente=request.user)
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([EsVendedor])
def retrieve_producto(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id, vendedor=request.user)
    except Producto.DoesNotExist:
        return Response({"error": "Producto no encontrado o no pertenece al usuario"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductoSerializer(producto)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([EsVendedor])
def update_producto(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id, vendedor=request.user)
    except Producto.DoesNotExist:
        return Response({"error": "Producto no encontrado o no pertenece al usuario"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductoSerializer(producto, data=request.data, context={'request': request}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "nombre": serializer.data['nombre'],
            "message": "Producto actualizado con éxito"
        }, status=status.HTTP_200_OK)

    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([EsVendedor])
def delete_producto(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id, vendedor=request.user)
    except Producto.DoesNotExist:
        return Response({"error": "Producto no encontrado o no pertenece al usuario"}, status=status.HTTP_404_NOT_FOUND)

    producto.delete()
    return Response({"message": "Producto eliminado con éxito"}, status=status.HTTP_204_NO_CONTENT)


# VISTAS PUBLICAS, CUALQUIER USUARIO PUEDE ACCEDER
# si no es vendedor indicar que no es vendedor
@api_view(['GET'])
def list_productos_vendedor(request, vendedor_id):
    try:
        vendedor = Cliente.objects.get(id=vendedor_id)
    except Cliente.DoesNotExist:
        return Response({"error": "Vendedor no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    productos = Producto.objects.filter(vendedor=vendedor)
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def retrieve_producto_vendedor(request, vendedor_id, producto_id):
    try:
        vendedor = Cliente.objects.get(id=vendedor_id)
    except Cliente.DoesNotExist:
        return Response({"error": "Vendedor no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    try:
        producto = Producto.objects.get(id=producto_id, vendedor=vendedor)
    except Producto.DoesNotExist:
        return Response({"error": "Producto no encontrado para este vendedor"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductoSerializer(producto)
    return Response(serializer.data, status=status.HTTP_200_OK)
