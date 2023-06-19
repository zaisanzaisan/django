# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
from rest_framework import generics
from .models import *
from .serializers import *


# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView

class SensorAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


class SensorAPIList(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


class MeasurementAPIList(generics.ListCreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
