import datetime
import random
from django.core.management.base import BaseCommand
from faker import Faker

from americana.models import Area, Tesis, Publicacion, Constancia, Autor

PROGRAMAS = ['Maestria', 'Doctorado']


class Command(BaseCommand):
    help = 'Create data to Tesis, Publicacion and Constancia'

    def handle(self, *args, **options):
        fake = Faker()
        fecha_2022 = datetime.datetime(year=2022, month=1, day=1)
        fecha_2021 = datetime.datetime(year=2021, month=1, day=1)
        fecha_2020 = datetime.datetime(year=2020, month=1, day=1)

        for i in range(5):
            Autor.objects.create(
                username=fake.user_name(), first_name=fake.first_name(),
                last_name=fake.last_name(), password=fake.password(),
                email=fake.company_email()
            )

        for i in range(100):
            area_random = random.choice(Area.objects.all())
            autor_random = random.choice(Autor.objects.all())
            fecha_random = random.choice([fecha_2020, fecha_2021, fecha_2022])
            data = {
                'file': fake.file_name(extension='pdf', category='office'),
                'title': f'Publicacion {i}', 'autor': autor_random,
                'area': area_random, 'conference': 'Acapulco',
                'description': fake.text(), 'isbn': fake.isbn13(),
                'publish_date': fecha_random
            }

            Publicacion.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Successfully Publicaciones data'))

        for i in range(100):
            area_random = random.choice(Area.objects.all())
            autor_random = random.choice(Autor.objects.all())
            programa_random = random.choice(PROGRAMAS)
            fecha_random = random.choice([fecha_2020, fecha_2021, fecha_2022])
            data = {
                'file': fake.file_name(extension='pdf', category='office'),
                'title': f'Tesis {i}', 'program': programa_random,
                'autor': autor_random, 'area': area_random,
                'director': fake.name(), 'co_director': fake.name(),
                'description': fake.text(), 'publish_date': fecha_random
            }

            Tesis.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Successfully Tesis data'))

        for i in range(100):
            area_random = random.choice(Area.objects.all())
            autor_random = random.choice(Autor.objects.all())
            fecha_random = random.choice([fecha_2020, fecha_2021, fecha_2022])
            data = {
                'file': fake.file_name(extension='pdf', category='office'),
                'title': f'Constancia {i}', 'autor': autor_random,
                'area': area_random, 'description': fake.text(),
                'publish_date': fecha_random
            }

            Constancia.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Successfully Constancias data'))
