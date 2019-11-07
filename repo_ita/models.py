from django.contrib.auth.models import User
from django.db import models

TYPES_OF_ARTICULES = (
    ('academico', 'Academico'),
    ('investigacion', 'Investigacion'),
    ('tesis', 'Tesis'),
)


class Articulo(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripcion')
    type_of_articule = models.CharField(
        max_length=20, choices=TYPES_OF_ARTICULES,
        verbose_name='Tipo de Documento')
    tags = models.CharField(max_length=50)
    file_path = models.FileField(
        upload_to='docs/', verbose_name='Archivo a Subir')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    upload_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Articulo: {self.name}"
