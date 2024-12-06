from decimal import Decimal
from django.conf import settings
from products.serializers import ProductoSerializer
from products.models import Producto

class Carro:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_KEY)
        if not cart:
            cart = self.session[settings.CART_SESSION_KEY] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, producto, cantidad=1, sobre_escribir=False):

        producto_id = str(producto["id"])
        if producto_id not in self.cart:
            self.cart[producto_id] = {
                "cantidad": 0,
                "precio": str(producto["precio"]),
            }
        if sobre_escribir:
            self.cart[producto_id]["cantidad"] = cantidad
        else:
            self.cart[producto_id]["cantidad"] += cantidad
        self.save()

    def remove(self, producto):
        producto_id = str(producto["id"])
        if producto_id in self.cart:
            del self.cart[producto_id]
            self.save()

    def __iter__(self):
        producto_ids = self.cart.keys()
        productos = Producto.objects.filter(id__in=producto_ids)
        carro = self.cart.copy()
        for producto in productos:
            carro[str(producto.id)]["producto"] = ProductoSerializer(producto).data
        for item in carro.values():
            item["precio"] = Decimal(item["precio"])
            item["total_precio"] = item["precio"] * item["cantidad"]
            yield item

    def __len__(self):
        return sum(item["cantidad"] for item in self.cart.values())

    def obtener_total_precio(self):
        return sum(Decimal(item["precio"]) * item["cantidad"] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_KEY]
        self.save()
