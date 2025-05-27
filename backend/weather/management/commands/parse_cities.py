import json

from django.core.management import BaseCommand

from weather.models import City


class Command(BaseCommand):
    help = "Добавляет в базу города России"

    def handle(self, *args, **options):
        with open("cities.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            for city in data:
                City.objects.get_or_create(
                    name=city["name"],
                    subject=city["subject"],
                    district=city["distict"],
                    latitude=city["latitude"],
                    longitude=city["longitude"],
                )
