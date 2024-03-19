from rest_framework import generics
from productos.serializers import ProductoSerializer
from productos.models import Producto

from prometheus_client import start_http_server, Summary
from django.http import HttpResponse

import time


# Crear un objeto Summary para medir el tiempo de respuesta de la vista
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

class ProductoListView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


class ProductoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

