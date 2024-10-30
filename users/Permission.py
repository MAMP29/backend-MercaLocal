from rest_framework import  permissions

'''
# Permiso para comprar productos
class CanBuyProduct(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.can_buy_product

'''


# Permiso relacionado con el apartado de vendedor
class EsVendedor(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_vendedor)