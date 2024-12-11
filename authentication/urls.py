from django.urls import path
from . import views



urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('convertir-vendedor', views.convertir_vendedor, name='convertir-vendedor'),
    path('es-vendedor', views.es_vendedor, name='es-vendedor'),
    path('logout', views.logout, name='logout'), # Nueva URL para logout

    # URL para probar el CAPTCHA de Cloudflare
    path('probar-turnstile', views.probar_turnstile, name='probar-turnstile'),
]