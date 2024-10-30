from django.contrib import admin
from .models import Cliente

# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'telefono', 'ciudad', 'is_staff', 'is_active','date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'telefono', 'ciudad')
    list_filter = ('is_staff', 'is_active', 'date_joined')

    fieldsets = (
        ('profile info', {
            'fields': ('first_name','last_name','email','telefono', 'ciudad')
        }),
        ('permissions', {
            'fields': ('is_staff','is_active') #'can_buy_product', 'can_sell_product')
        }),
    )

admin.site.register(Cliente, ClienteAdmin)