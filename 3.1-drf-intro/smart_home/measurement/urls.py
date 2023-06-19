from django.urls import path
from .views import *

urlpatterns = [
    # TODO: зарегистрируйте необходимые маршруты
    path('detail/sensor/<int:pk>/', SensorAPIDetail.as_view(), name='detail_sensor'),  # просмотр, удаление, обновление
    # датчика    http://127.0.0.1:8000/api/detail/sensor/1/
    path('list/sensor/', SensorAPIList.as_view(), name='list-sensor'),  # просмотр списка всех датчиков или создать один
    # датчик   http://127.0.0.1:8000/api/list/sensor/
    path('list/measurement/', MeasurementAPIList.as_view(), name='list-measurement'),  # просмотр списка всех измерений
    # или создать одно измерение     http://127.0.0.1:8000/api/list/measurement/
]
