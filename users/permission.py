from rest_framework import  permissions

# Permiso relacionado con el apartado de vendedor
class EsVendedor(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.es_vendedor)