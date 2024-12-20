"""
URL configuration for localstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('producto/', include('products.urls')),
    path('carrito/', include('cart.urls')),
    path('pedido/', include('order.urls')),
    path('favoritos/', include('favs.urls')),
    #path('accounts/', include('allauth.urls')), # Cargando las urls de allauth
    #path('accounts/profile/', include('dashboard.urls')), # Empleamos un perfil básico para que lo muestre al iniciar sesión

]
# Agregar configuración para archivos de medios
if settings.DEBUG:  # Solo para desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
