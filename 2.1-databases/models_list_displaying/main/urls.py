
from django.contrib import admin
from django.urls import path

from books.views import books_view, books_by_date

urlpatterns = [
    path('books/', books_view, name='books'),
    path('admin/', admin.site.urls),
    path('books/<str:pub_date>/', books_by_date, name='books_by_date'),
]
