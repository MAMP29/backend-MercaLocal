from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from products.serializers import ProductoSerializer
from products.models import Producto
from .service import Carro

# Create your views here.

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def listar_carrito(request):
    carro = Carro(request)
    productos = list(carro)
    total_precio = carro.obtener_total_precio()
    return Response({
        "productos": productos,
        "total_precio": total_precio
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def agregar_producto(request):
    producto_id = request.data.get('producto_id')
    cantidad = request.data.get('cantidad', 1)
    sobre_escribir = request.data.get("sobre_escribir", False)

    try:
        producto = Producto.objects.get(id=producto_id)
    except Producto.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    # Verificar que la cantidad solicitada no exceda el stock
    if int(cantidad) > producto.stock:
        return Response({
            "error": "Cantidad solicitada excede el stock disponible",
            "stock_disponible": producto.stock
        }, status=status.HTTP_400_BAD_REQUEST)

    carro = Carro(request)
    carro.add(producto={"id": producto.id, "precio": producto.precio}, cantidad=int(cantidad), sobre_escribir=sobre_escribir)
    return Response({"message": "Cantidad del producto añadida con éxito"}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def actualizar_carrito(request):
    producto_id = request.data.get('producto_id')
    cantidad = request.data.get('cantidad', 1)

    try:
        producto = Producto.objects.get(id=producto_id)
    except Producto.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    # Verificar que la cantidad solicitada no exceda el stock
    if int(cantidad) > producto.stock:
        return Response({
            "error": "Cantidad solicitada excede el stock disponible",
            "stock_disponible": producto.stock
        }, status=status.HTTP_400_BAD_REQUEST)

    carro = Carro(request)
    carro.add(producto={"id": producto.id, "precio": producto.precio}, cantidad=int(cantidad), sobre_escribir=True)
    return Response({"message": "Cantidad del producto actualizada con éxito"}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def eliminar_producto(request):
    producto_id = request.data.get('producto_id')

    try:
        producto = Producto.objects.get(id=producto_id)
    except Producto.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    carro = Carro(request)
    carro.remove(producto={"id": producto.id})
    return Response({"message": "Producto eliminado con éxito"}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vaciar_carrito(request):
    carro = Carro(request)
    carro.clear()
    return Response({"message": "Carrito vaciado con éxito"}, status=status.HTTP_200_OK)
