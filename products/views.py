from rest_framework.decorators import api_view
from urllib3 import request

from users.permission import EsVendedor
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from products.serializers import ProductoSerializer, ProductoCreateSerializer, ProductoUpdateSerializer
from .models import Producto, Categoria
from users.models import Cliente
from django_filters.rest_framework import DjangoFilterBackend
from .product_filter import ProductFilter
from rest_framework.generics import ListAPIView
# Create your views here.


# Función para crear un producto solo si es un vendedor

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([EsVendedor])
def create_producto(request):
    serializer = ProductoCreateSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        serializer.save()
        return Response({
            "nombre": serializer.data['nombre'],
            "message": "Producto creado con éxito"
        }, status=status.HTTP_201_CREATED)

    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([EsVendedor])
def list_mis_productos(request):
    productos = Producto.objects.filter(vendedor=request.user).all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Función para listar todos los productos del usuario que es vendedor
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
#@permission_classes([EsVendedor])
def list_productos(request):
    productos = Producto.objects.select_related('categoria').all()
    serializer = ProductoSerializer(productos, many=True, context={'request': request})
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

    serializer = ProductoUpdateSerializer(producto, data=request.data, context={'request': request}, partial=True)
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


# Buscar productos por categoria, en deshuso por el momento, para ello emplee el filtro de django-filters para hacer el filtrado en la API de abajo
@api_view(['GET'])
def listar_productos_por_categoria(request, categoria_id):
    try:
        categoria = Categoria.objects.get(id=categoria_id)
    except Categoria.DoesNotExist:
        return Response({"error": "Categoria no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    productos = Producto.objects.filter(categoria=categoria)
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Buscar productos por filtro
class ProductoListView(ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return super().get_serializer(*args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    