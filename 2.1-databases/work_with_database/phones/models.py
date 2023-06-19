from django.db import models


class Phone(models.Model):
    # TODO: Добавьте требуемые поля
    id = models.PositiveIntegerField(primary_key=True, verbose_name='Идентификатор товара')
    name = models.CharField(max_length=100, verbose_name='Наименование товара')
    price = models.IntegerField(verbose_name='Цена товара')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True, verbose_name='Фото товара')
    release_date = models.DateField(verbose_name='Дата добавления')
    lte_exists = models.BooleanField(default=False, verbose_name='Наличие функции LTE')
    slug = models.SlugField(max_length=150, unique=True, verbose_name='URL товара')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'

