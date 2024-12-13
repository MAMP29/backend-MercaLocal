from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from users.models import Cliente
from favs.models import Favorito
from products.models import Producto, Categoria

class FavoritosTests(APITestCase):

    def setUp(self):
        # Crear usuario y token
        self.user = Cliente.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="securepassword123",
            first_name="Test",
            last_name="User",
            telefono=3123456789,
            ciudad="Test City"
        )
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Crear categoría para el producto
        self.categoria = Categoria.objects.create(
            nombre="Categoría de prueba"
        )

        # Crear producto para pruebas
        self.producto = Producto.objects.create(
            id=1,
            nombre="Producto de prueba",
            descripcion="Descripción del producto de prueba",
            precio=100.00,
            imagen="ruta/a/la/imagen.jpg",
            vendedor_id=1,
            categoria_id=self.categoria.id
        )

        
        self.add_favorito_url = '/favoritos/anadir'
        self.listar_favoritos_url = '/favoritos/listar'
        self.delete_favorito_url = lambda pk: f'/favoritos/borrar/{pk}'

    def test_add_favorito(self):
        #Prueba que un usuario puede añadir un producto a sus favoritos
        response = self.client.post(self.add_favorito_url, {
            'producto_id': self.producto.id
        }, format='json')

        print("Respuesta del servidor:", response.status_code, response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('producto', response.json())
        self.assertEqual(response.json()['producto']['id'], self.producto.id)
        self.assertEqual(response.json()['producto']['nombre'], self.producto.nombre)

    def test_add_favorito_no_existente(self):
        #Prueba que intentar añadir un producto que no existe devuelve un error 400
        response = self.client.post(self.add_favorito_url, {
            'producto_id': 999  # ID inexistente
        }, format='json')

        print("Respuesta del servidor:", response.status_code, response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('producto_id', response.json())
        self.assertIn('object does not exist', response.json()['producto_id'][0])

    def test_listar_favoritos(self):
        #Prueba que un usuario puede listar sus favoritos.
        # Añadir un producto a favoritos primero
        Favorito.objects.create(cliente=self.user, producto=self.producto)

        response = self.client.get(self.listar_favoritos_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)  # Verificar que hay un favorito en la respuesta
        favorito = response.json()[0]
        self.assertEqual(favorito['producto']['id'], self.producto.id)
        self.assertEqual(favorito['producto']['nombre'], self.producto.nombre)

    def test_delete_favorito(self):
        #Prueba que un usuario puede eliminar un favorito
        # Añadir un producto a favoritos primero
        favorito = Favorito.objects.create(cliente=self.user, producto=self.producto)

        response = self.client.delete(self.delete_favorito_url(self.producto.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Favorito.objects.filter(id=favorito.id).exists())

    def test_delete_favorito_not_found(self):
        #Prueba que eliminar un favorito que no existe devuelve 404
        response = self.client.delete(self.delete_favorito_url(999))  # ID inexistente

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Favorito no encontrado', response.content.decode())
