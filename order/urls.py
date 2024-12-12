from django.urls import path
from . import views

urlpatterns = [
    path('pedir-productos', views.checkout, name='pedir-productos'),
    path('obtener-detalle/<int:pedido_id>', views.obtener_detalle, name='obtener-detalle'),
    path('obtener-pedidos', views.obtener_pedido, name='obtener-pedidos'),

    path('reporte-productos-mas-vendidos', views.ReporteProductosMasVendidos.as_view(), name='reporte-productos-mas-vendidos'),
    path('reporte-ventas-mensuales', views.ReporteVentasMensualesAPIView.as_view(), name='reporte-ventas-mensuales'),
    path('reporte-ventas-por-mes/', views.ReporteVentasMes.as_view(), name='reporte-ventas-por-mes'),
]