from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.utils import timezone
from users.models import Cliente
from products.models import Producto, Categoria
from order.models import Pedido, DetallePedido

# Create your tests here.
class PedidoTests(APITestCase):
    def setUp(self):
        # Crear usuario cliente
        self.cliente = Cliente.objects.create_user(
            username="cliente",
            email="cliente@example.com",
            password="password123",
            telefono="3123456789",
        )
        self.cliente_token, _ = Token.objects.get_or_create(user=self.cliente)

        # Crear usuario vendedor
        self.vendedor = Cliente.objects.create_user(
            username="vendedor",
            email="vendedor@example.com",
            password="password123",
            telefono="3123456789",
            es_vendedor=True,
            nombre_tienda="Tienda del Vendedor"
        )
        self.vendedor_token, _ = Token.objects.get_or_create(user=self.vendedor)

        # Crear categoría y producto
        self.categoria = Categoria.objects.create(nombre="Categoría de prueba")
        self.producto = Producto.objects.create(
            nombre="Producto de prueba",
            precio=100.0,
            stock=10,
            categoria=self.categoria,
            vendedor=self.vendedor
        )
        # URLs
        self.checkout_url = '/pedido/pedir-productos'
        self.obtener_pedido_url = '/pedido/obtener-pedidos'
        self.obtener_detalle_url = lambda pedido_id: f'/pedido/obtener-detalle/{pedido_id}'
        self.reporte_productos_mas_vendidos_url = '/pedido/reporte-productos-mas-vendidos'
        self.reporte_ventas_mensuales_url = '/pedido/reporte-ventas-mensuales'
        self.reporte_ventas_mes_url = '/pedido/reporte-ventas-por-mes/'

    def test_checkout(self):
        # Prueba que un cliente puede realizar un pedido
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.cliente_token.key}')
        data = {
            "pedido": {"total": 200.0, "direccion": "Calle de prueba 123"},
            "detalle": {
                "1": {"producto": self.producto.id, "cantidad": 2, "precio": 100.0}
            }
        }
        response = self.client.post(self.checkout_url, data, format='json')
        print("Respuesta del servidor:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('pedido', response.data)
        self.assertEqual(response.data['message'], "Pedido creado con éxito")

    def test_obtener_detalle(self):
        # Prueba que se puedan obtener los detalles de un pedido
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.cliente_token.key}')
        pedido = Pedido.objects.create(cliente=self.cliente, total=200.0, estado='pendiente')
        DetallePedido.objects.create(pedido=pedido, producto=self.producto, cantidad=2, precio=100.0)
        response = self.client.get(self.obtener_detalle_url(pedido.id))
        print("Respuesta del servidor:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['pedido_id'], pedido.id)
        self.assertEqual(len(response.data['detalles']), 1)

    def test_obtener_pedido(self):
        # Prueba que un cliente pueda obtener sus pedidos
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.cliente_token.key}')
        Pedido.objects.create(cliente=self.cliente, total=200.0, estado='pendiente')
        response = self.client.get(self.obtener_pedido_url)
        print("Respuesta del servidor:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_reporte_productos_mas_vendidos(self):
        # Prueba que un vendedor pueda obtener el reporte de productos más vendidos
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.vendedor_token.key}')
        pedido = Pedido.objects.create(cliente=self.cliente, total=200.0, estado='pendiente')
        DetallePedido.objects.create(pedido=pedido, producto=self.producto, cantidad=2, precio=100.0)
        response = self.client.get(self.reporte_productos_mas_vendidos_url)
        print("Respuesta del servidor:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nombre_producto'], self.producto.nombre)
        self.assertEqual(response.data[0]['total_vendido'], 2)

    def test_reporte_ventas_mensuales(self):
        # Prueba que un vendedor pueda obtener un reporte de ventas mensuales
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.vendedor_token.key}')
        pedido = Pedido.objects.create(cliente=self.cliente, total=200.0, estado='pendiente')
        DetallePedido.objects.create(pedido=pedido, producto=self.producto, cantidad=2, precio=100.0)
        response = self.client.get(self.reporte_ventas_mensuales_url)
        print("Respuesta del servidor:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn('total_productos', response.data[0])
        self.assertIn('total_ganancias', response.data[0])

    def test_reporte_ventas_mes(self):
        #Prueba que un vendedor pueda obtener el reporte de ventas para un mes específico."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.vendedor_token.key}')
        pedido = Pedido.objects.create(cliente=self.cliente, total=200.0, estado='pendiente')
        DetallePedido.objects.create(pedido=pedido, producto=self.producto, cantidad=2, precio=100.0)
        response = self.client.get(self.reporte_ventas_mes_url, {'mes': timezone.now().strftime('%Y-%m')})
        print("Respuesta del servidor:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Resumen', response.data)
        self.assertIn('TotalProductos', response.data['Resumen'])
