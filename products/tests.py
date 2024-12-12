from rest_framework.test import APITestCase
from rest_framework import status
from users.models import Cliente
from products.models import Producto, Categoria
from rest_framework.authtoken.models import Token
from django.urls import reverse

class ProductoTests(APITestCase):

    def setUp(self):
        # Crear un cliente para pruebas
        self.cliente = Cliente.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="securepassword123",
            first_name="Test",
            last_name="User",
            telefono=3123456789,
            ciudad="Test City"
        )
        self.client.es_vendedor= True
        self.token = Token.objects.create(user=self.cliente)
        
        # Crear categorías para productos
        self.categoria = Categoria.objects.create(nombre="Electrónica")
        
        # Crear productos para pruebas
        self.producto = Producto.objects.create(
            nombre="Laptop",
            precio=1000.00,
            stock=10,
            descripcion="Laptop de prueba",
            vendedor=self.cliente,
            categoria=self.categoria,
            imagen="test_image.jpg"
        )

    def test_create_producto(self):
        # Crear producto
        url = '/crear-producto'
        data = {
            "nombre": "Producto de prueba",
            "precio": 100.00,
            "stock": 10,
            "descripcion": "Descripción del producto",
            "imagen": "image_url",
            "vendedor": self.cliente.id,
            "categoria": self.categoria.id
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_list_productos(self):
        # Prueba para listar productos
        url = reverse('listar-productos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_retrieve_producto(self):
        # Prueba para obtener un producto específico
        url = reverse('producto', args=[self.producto.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], self.producto.nombre)

    def test_update_producto(self):
        # Prueba para actualizar un producto existente
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('actualizar-producto', args=[self.producto.id])
        data = {
            "nombre": "Laptop Actualizada",
            "precio": "1200.00",
            "stock": 8,
            "descripcion": "Laptop actualizada de prueba",
            "categoria": self.categoria.id,
            "imagen": "updated_image.jpg"
        }
        response = self.client.put(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], "Laptop Actualizada")

    def test_delete_producto(self):
        # Prueba para borrar un producto existente
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('eliminar-producto', args=[self.producto.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_productos_vendedor(self):
        # Prueba para listar productos de un vendedor específico
        url = reverse('listar-productos-vendedor', args=[self.cliente.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_retrieve_producto_vendedor(self):
        # Prueba para obtener un producto específico de un vendedor
        url = reverse('producto-vendedor', args=[self.cliente.id, self.producto.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], self.producto.nombre)
