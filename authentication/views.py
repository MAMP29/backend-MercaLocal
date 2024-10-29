from allauth.core.internal.httpkit import serialize_request
from lib2to3.btm_utils import tokens

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from users.serializers import ClienteSerializer
from users.models import Cliente
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated # Permite validar si un usuario esta autenticado y a que rutas puede acceder
from rest_framework.authentication import TokenAuthentication

# Create your views here.
# Clase encargada de la respuesta al cliente en base al servición de autenticación


# Para logear el usuario
@api_view(['POST'])
def login(request):

    # Obtenemos el usuario si existe por su nombre de usuario, si no existe, devolvemos un 404
    cliente = get_object_or_404(Cliente, username=request.data['username'])

    # Verificamos la contraseña del usuario
    if not cliente.check_password(request.data['password']):
        return Response({"error":"Invalid password"}, status=status.HTTP_400_BAD_REQUEST)

    # Creamos un token
    token, created = Token.objects.get_or_create(user=cliente)
    serializer = ClienteSerializer(instance=cliente) # Usuario convertido en JSON

    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)

# Para registrar el usuario
@api_view(['POST'])
def register(request):
    serializer = ClienteSerializer(data=request.data)

    print(request.data)
    print("------------------------")

    if serializer.is_valid():
        cliente = serializer.save()

        token = Token.objects.create(user=cliente)
        return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)



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
