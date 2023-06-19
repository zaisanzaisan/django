import csv

from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for p in phones:
            # TODO: Добавьте сохранение модели
            Phone(
                id=p['id'],
                name=p['name'],
                image=p['image'],
                price=p['price'],
                release_date=p['release_date'],
                lte_exists=p['lte_exists'],
                slug=p['name'].replace(' ', '-')
            ).save()

