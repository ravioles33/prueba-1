from rest_framework import generics
from productos.serializers import ProductoSerializer
from productos.models import Producto

from prometheus_client import start_http_server, Summary
from django.http import HttpResponse

import time

from silk.profiling.profiler import silk_profile

# Crear un objeto Summary para medir el tiempo de respuesta de la vista
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

class ProductoListView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    @silk_profile(name='ProductoListView dispatch')
    def dispatch(self, *args, **kwargs):
        with REQUEST_TIME.time():
            return super().dispatch(*args, **kwargs)

class ProductoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    @silk_profile(name='ProductoDetailView dispatch')
    def dispatch(self, *args, **kwargs):
        with REQUEST_TIME.time():
            return super().dispatch(*args, **kwargs)

# Función de vista para medir el tiempo de respuesta
@REQUEST_TIME.time()
def my_view(request):
    # Lógica de tu vista
    time.sleep(1)  # Simula algún trabajo que tome tiempo
    return HttpResponse("OK")

from prometheus_client import generate_latest

def metrics(request):
    return HttpResponse(generate_latest(), content_type="text/plain")
