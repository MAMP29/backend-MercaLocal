from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from .serializers import DetallePedidoSerializer
from products.models import Producto
from users.models import Cliente
from cart.service import Carro
from .models import Pedido, DetallePedido


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic
def checkout(request):
    carro = Carro(request)
    if len(carro) == 0:
        return Response({"error": "No hay productos en el carrito"}, status=status.HTTP_400_BAD_REQUEST)

    # Crear el pedido
    pedido = Pedido.objects.create(
        cliente=request.user,
        total=carro.obtener_total_precio(),
        estado='pendiente'
    )


    # Crear los detalles del pedido
    for producto in carro:
        producto_obj = Producto.objects.get(id=producto["producto"]["id"])
        vendedor_nombre = producto_obj.vendedor.nombre_tienda  # Obtener el nombre del vendedor dinámicamente
        print("ESTE ES EL NOMBRE de la tienda", vendedor_nombre)

        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto_obj,
            cantidad=producto["cantidad"],
            precio=producto["precio"],
        )

    # Vaciar el carrito
    carro.clear()

    return Response({
        "pedido": pedido.id,
        "message": "Pedido creado con éxito"
    }, status=status.HTTP_201_CREATED)


# Función para obtener los detalles del pedido
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def obtener_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    detalles = DetallePedido.objects.filter(pedido=pedido)
    serializer = DetallePedidoSerializer(detalles, many=True)

    return Response({
        "pedido_id": pedido.id,
        "detalles": serializer.data,  # Incluye los nombres de los vendedores
    }, status=status.HTTP_200_OK)