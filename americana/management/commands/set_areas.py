from django.core.management.base import BaseCommand
from americana.models import Area

DATA = [
    'Artes y Humanidades',
    'Biologia y Química',
    'Biotecnologia y Ciencias Agropecuarias',
    'Ciencias Sociales y Económicas',
    'Físico Matemáticas y Ciencias de la Tierra',
    'Ingenierías',
    'Medicina y Ciencias de la Salud',
    'Multidisciplina',
]


class Command(BaseCommand):
    help = 'Create data for Area'

    def handle(self, *args, **options):
        for d in DATA:
            Area.objects.create(name=d)
            self.stdout.write(self.style.SUCCESS('Successfully create data'))
