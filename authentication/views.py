import requests
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from users.serializers import ClienteSerializer, ConvertirVendedorSerializer    # VendedorSerializer
from users.models import Cliente
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated # Permite validar si un usuario esta autenticado y a que rutas puede acceder
from rest_framework.authentication import TokenAuthentication
from users.permission import EsVendedor
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

# Create your views here.
# Clase encargada del api rest de la autenticación para los clientes


# Para logear el usuario
@api_view(['POST'])
def login(request):

    print(request.data)

    # Obtenemos el usuario si existe por su nombre de usuario, si no existe, devolvemos un 404
    cliente = get_object_or_404(Cliente, email=request.data['email'])

    # Verificamos la contraseña del usuario
    if not cliente.check_password(request.data['password']):
        return Response({"error":"Invalid password"}, status=status.HTTP_400_BAD_REQUEST)

    # Creamos un token o obtenemos uno ya existente del cliente
    token, created = Token.objects.get_or_create(user=cliente)
    serializer = ClienteSerializer(instance=cliente) # Usuario convertido en JSON

    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)

# Para registrar el usuario
@api_view(['POST'])
def register(request):

    # Verificamos si el usuario ha pasado la captcha
    if not settings.DEBUG:
        if not verify_turnstile(request.data['turnstile_token']):
            return Response({"error": "Captcha incorrecto"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ClienteSerializer(data=request.data)

    print(request.data)
    print("------------------------")

    if serializer.is_valid():
        cliente = serializer.save()
        cliente.is_active = False
        cliente.save()

        uid = urlsafe_base64_encode(force_bytes(cliente.id))
        token = default_token_generator.make_token(cliente)
        activate_url = f"http://localhost:8000/validar-email/{uid}/{token}/"

        send_mail(
            subject='Activación de cuenta',
            message=f'Por favor, activa tu cuenta haciendo clic en el siguiente enlace: {activate_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[cliente.email],
        )
        return Response({"detail": "Registro exitoso. Revisa tu correo para activar la cuenta."}, status=201)
    #print(request.data)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Para recuperar datos de perfil en base a un token (solo si es valido)
@api_view(['POST'])
@authentication_classes([TokenAuthentication]) # Necesitamos enviar un header con token el cual se validará
@permission_classes([IsAuthenticated])
def profile(request):

    print(request.user)
    #return Response("You are login with {}".format(request.user.username), status=status.HTTP_200_OK)

    serializer = ClienteSerializer(instance=request.user)

    return Response(serializer.data, status=status.HTTP_200_OK)



# Para convertir un cliente en un vendedor
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def convertir_vendedor(request):

    cliente = Cliente.objects.get(email=request.data['email'])


    if cliente.es_vendedor:
        return Response({"error":"El usuario ya es un vendedor"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ConvertirVendedorSerializer(cliente, data=request.data)

    print(request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "nombre_tienda": serializer.data['nombre_tienda'],
            "message": "El usuario ha sido convertido en un vendedor"
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Para saber si un usuario es vendedor
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([EsVendedor])
def es_vendedor(request):
    return Response({"es_vendedor": request.user.es_vendedor}, status=status.HTTP_200_OK)

# Para cerrar sesion de un usuario
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    # Eliminar el token del usuario
    request.user.auth_token.delete()
    return Response(
        {"detail": "Sesión cerrada exitosamente"},
        status=status.HTTP_200_OK
    )


def verify_turnstile(captcha_response):
    """Verifica el CAPTCHA usando la clave secreta de Cloudflare."""
    secret_key = settings.TURNSTILE_SECRET_KEY
    verify_url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'

    data = {
        'secret': secret_key,
        'response': captcha_response
    }

    response = requests.post(verify_url, data=data)
    result = response.json()

    return result.get('success', False)

def probar_turnstile(request):
    """Probar el CAPTCHA usando la clave secreta de Cloudflare."""

    captcha_response = 'RESPUESTA_DE_EJEMPLO'

    if verify_turnstile(captcha_response):
        return JsonResponse({'status': 'success', 'message': 'Captcha validado correctamente.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Captcha no valido.'})


@api_view(['GET'])
def validar_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(Cliente, pk=uid)
        
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Cuenta activada exitosamente"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Token de activación inválido"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"error": "Token de activación inválido"}, status=status.HTTP_400_BAD_REQUEST)