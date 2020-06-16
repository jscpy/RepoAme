# Generated by Django 2.2.7 on 2019-11-08 04:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import repo_ita.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('description', models.TextField(verbose_name='Descripcion')),
                ('type_of_articule', models.CharField(choices=[('academico', 'Academico'), ('investigacion', 'Investigacion'), ('tesis', 'Tesis')], max_length=20, verbose_name='Tipo de Documento')),
                ('tags', models.CharField(max_length=50)),
                ('file_path', models.FileField(upload_to=repo_ita.models.user_directory_path, verbose_name='Archivo a Subir')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('upload_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
