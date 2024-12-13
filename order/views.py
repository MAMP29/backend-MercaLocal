from django.db import transaction
from django.db.models import F, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from django.utils.dateparse import parse_date
from users.permission import EsVendedor
from .serializers import DetallePedidoSerializer, PedidoSerializer
from products.models import Producto
from users.models import Cliente
from cart.service import Carro
from .models import Pedido, DetallePedido
from rest_framework.views import APIView
from django.utils import timezone
from datetime import datetime, timedelta



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic
def checkout(request):
    #carro = Carro(request)
    #if len(carro) == 0:
        #return Response({"error": "No hay productos en el carrito"}, status=status.HTTP_400_BAD_REQUEST)
    pedido = request.data['pedido']
    detalle = request.data['detalle']
    # Crear el pedido
    newpedido = Pedido.objects.create(
        cliente=request.user,
        total=pedido['total'],
        estado='pendiente',
        direccion= pedido['direccion']
    )
    # Crear los detalles del pedido
    for producto in detalle.values():
        producto_obj = Producto.objects.get(id=producto["producto"])
        vendedor_nombre = producto_obj.vendedor.nombre_tienda  # Obtener el nombre del vendedor dinámicamente
        print("ESTE ES EL NOMBRE de la tienda", vendedor_nombre)

        DetallePedido.objects.create(
            pedido=newpedido,
            producto=producto_obj,
            cantidad=producto["cantidad"],
            precio=producto["precio"],
        )

    # Vaciar el carrito
    #carro.clear()

    return Response({
        "pedido": newpedido.id,
        "message": "Pedido creado con éxito"
    }, status=status.HTTP_201_CREATED)


# Función para obtener los detalles del pedido
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def obtener_detalle(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    detalles = DetallePedido.objects.filter(pedido=pedido)
    serializer = DetallePedidoSerializer(detalles, many=True)

    return Response({
        "pedido_id": pedido.id,
        "detalles": serializer.data,  # Incluye los nombres de los vendedores
    }, status=status.HTTP_200_OK)

# Función para obtener los detalles del pedido
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def obtener_pedido(request):
    pedido = Pedido.objects.filter(cliente_id=request.user)
    serializer = PedidoSerializer(pedido, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Funcion para generar reporte de los pedidos más vendidos
class ReporteProductosMasVendidos(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [EsVendedor]

    def get(self, request, *args, **kwargs):
        vendedor = request.user

        # Obtener productos vendidos filtrados por el vendedor
        productos_vendidos = (
            DetallePedido.objects.filter(producto__vendedor=vendedor, pedido__estado='pendiente') # Solo se consideran los pedidos pendientes, ya que no esta habilitado el envio de los mismos
            .values(nombre_producto=F('producto__nombre'))
            .annotate(total_vendido=Sum('cantidad'))
            .order_by('-total_vendido')[:10]  # Los 10 más vendidos
        )

        return Response(productos_vendidos)

# Número de productos y ganancias por 6 meses
class ReporteVentasMensualesAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [EsVendedor]

    def get(self, request, *args, **kwargs):
        vendedor = request.user

        fecha_hoy = timezone.now()
        fecha_inicio = fecha_hoy - timedelta(days=180) # 180 días atrás

        ventas_mensuales = (
            DetallePedido.objects.filter(
                producto__vendedor=vendedor,
                pedido__estado='pendiente',  # Solo pedidos pendientes, ya que no esta habilitado el envio de los mismos
                pedido__fecha_creacion__gte=fecha_inicio
            )
            .annotate(mes=TruncMonth('pedido__fecha_creacion'))
            .values(mes=F('mes'))
            .annotate(
                total_productos=Sum('cantidad'),  # Número de productos vendidos
                total_ganancias=Sum(F('cantidad') * F('precio'))  # Ganancias totales
            )
            .order_by('mes')  # Ordenar por mes
        )

        datos = [
            {
                "mes": venta["mes"].strftime("%Y-%m"),
                "total_productos": venta["total_productos"],
                "total_ganancias": float(venta["total_ganancias"]),
            }
            for venta in ventas_mensuales
        ]

        return Response(datos)

# Número de ventas por un mes en especifico
class ReporteVentasMes(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [EsVendedor]

    def get(self, request, *args, **kwargs):
        vendedor = request.user
        mes_anio = request.query_params.get('mes', None)  # Obtener el mes desde los parámetros de consulta

        if mes_anio is None:
            mes_anio = timezone.now().strftime('%m')

        try:
            # Convertir `mes` a un objeto datetime
            mes_inicio = datetime.strptime(mes_anio, '%Y-%m')

            mes_inicio = timezone.make_aware(mes_inicio, timezone.get_current_timezone())

            mes_fin = (mes_inicio.replace(day=28) + timedelta(days=4)).replace(day=1)  # Inicio del próximo mes
        except ValueError:
            return Response({"error": "El formato del mes debe ser YYYY-MM."}, status=400)

        # Consultar los datos para el mes específico
        productos_vendidos = (
            DetallePedido.objects.filter(
                producto__vendedor=vendedor,
                pedido__estado='pendiente',  # Solo pedidos pendientes
                pedido__fecha_creacion__gte=mes_inicio,
                pedido__fecha_creacion__lt=mes_fin
            )
            .values(nombre_producto=F('producto__nombre'))
            .annotate(
                cantidad_vendida=Sum('cantidad'),  # Sumar las cantidades vendidas
                total_ganancias=Sum(F('cantidad') * F('precio'))  # Calcular las ganancias por producto
            )
        )

        # Construir el formato solicitado
        reporte = {
            "productos": [],
            "resumen": {
                "total_productos": 0,
                "total_ganancias": 0
            }
        }
        total_productos = 0
        total_ganancias = 0

        for producto in productos_vendidos:
            reporte["productos"].append({
                "nombre_producto": producto["nombre_producto"],
                "cantidad": producto["cantidad_vendida"],
                "total": float(producto["total_ganancias"])
            })
            total_productos += producto["cantidad_vendida"]
            total_ganancias += producto["total_ganancias"]

        # Agregar los totales al reporte
        reporte["resumen"] = {
            "total_productos": total_productos,
            "total_ganancias": float(total_ganancias)
        }

        return Response(reporte)
