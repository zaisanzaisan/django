
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static


import phones.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', phones.views.index),
    path('catalog/', phones.views.show_catalog, name='catalog'),
    path('catalog/<slug:slug>/', phones.views.show_product, name='phone'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)