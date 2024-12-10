from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from favs.serializers import FavoritoSerializer
from .models import Favorito
from users.models import Cliente
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated # Permite validar si un usuario esta autenticado y a que rutas puede acceder

# Create your views here.


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_favorito(request):
    serializer = FavoritoSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({
            "producto":  serializer.data['producto'],
            "message": "Producto añadido a tus favoritos"
        }, status=status.HTTP_201_CREATED)

    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def listar_favoritos(request):
    favoritos = Favorito.objects.filter(cliente=request.user)
    serializer = FavoritoSerializer(favoritos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_favorito(request, pk):
    try:
        # Buscar el favorito solo si pertenece al usuario actual
        favorito = Favorito.objects.get(pk=pk, cliente=request.user)
    except Favorito.DoesNotExist:
        return Response({'detail': 'Favorito no encontrado o no pertenece al usuario.'}, status=status.HTTP_404_NOT_FOUND)

    # Eliminar el favorito
    favorito.delete()
    return Response(
        {'detail': 'Favorito eliminado con éxito.'},
        status=status.HTTP_204_NO_CONTENT
    )