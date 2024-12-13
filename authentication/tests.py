from rest_framework.test import APITestCase
from rest_framework import status
from users.models import Cliente
from rest_framework.authtoken.models import Token

# Create your tests here.
class AuthenticationTests(APITestCase):

    def setUp(self):
        # Crear un cliente para pruebas
        self.cliente = Cliente.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="securepassword123",
            first_name="Test",
            last_name="User",
            telefono=3123456789,
            ciudad="Test City",
        )
        self.token = Token.objects.create(user=self.cliente)

    def test_register_user(self):
        # Prueba para registrar un nuevo usuario
        fake_turnstile_token = "1x00000000000000000000AA"
        url = '/register'
        data = {
            "username":"newuser",
            "email": "newuser@example.com",
            "password": "newsecurepassword",
            "first_name": "New",
            "last_name": "User",
            "telefono": 3234567890,
            "ciudad": "New City",
            "turnstile_token": fake_turnstile_token
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["detail"], "Registro exitoso. Revisa tu correo para activar la cuenta.")

    def test_login_valid_user(self):
        # Prueba de login con credenciales válidas
        url = '/login'
        data = {"email": self.cliente.email, "password": "securepassword123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_invalid_password(self):
        # Prueba de login con contraseña incorrecta
        url = '/login'
        data = {"email": self.cliente.email, "password": "wrongpassword"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_profile_authenticated_user(self):
        # Prueba para recuperar el perfil con un token válido
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/profile'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.cliente.email)

    def test_profile_unauthenticated_user(self):
        # Prueba para recuperar perfil sin token
        url = '/profile'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_convertir_vendedor(self):
        # Prueba para convertir un cliente en vendedor
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/convertir-vendedor'
        data = {"email": self.cliente.email, "nombre_tienda": "Test Store"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre_tienda'], "Test Store")

    def test_es_vendedor_permission(self):
        # Prueba de acceso a ruta para vendedores
        self.cliente.es_vendedor = True
        self.cliente.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/es-vendedor'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['es_vendedor'], True)

    def test_logout(self):
        # Prueba de cierre de sesión
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/logout'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.cliente).exists())