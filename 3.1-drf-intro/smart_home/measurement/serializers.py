from rest_framework import serializers
from .models import *


class MeasurementSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=True, use_url=True,
                                   required=False)

    class Meta:
        model = Measurement
        fields = ['temperature', 'measurement_date', 'image']


class SensorDetailSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']
