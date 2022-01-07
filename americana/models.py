from django.db import models

class Tesis(models.Model):
    
    PROGRAMAS = (
        ('Maestria', 'Maestria',),
        ('Doctorado', 'Doctorado',),
    )
    
    file = models.FileField(upload_to='docs/tesis/', verbose_name='Documento')
    title = models.CharField(max_length=100, verbose_name='Titulo')
    autor = models.CharField(max_length=100, verbose_name='Autor')
    program = models.CharField(max_length=100, choices=PROGRAMAS, verbose_name='Programa')
    director = models.CharField(max_length=100, verbose_name='Director')
    co_director = models.CharField(max_length=100, verbose_name='Co-director')
    publish_date = models.DateField(verbose_name='Fecha de Publicacion')
    description = models.TextField(verbose_name='Resumen')
    created_at = models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tesis'
        verbose_name_plural = 'Tesis'
        ordering = ('id',)


class Publicacion(models.Model):
    file = models.FileField(upload_to='docs/publicaciones/', verbose_name='Documento')
    title = models.CharField(max_length=100, verbose_name='Titulo')
    autor = models.CharField(max_length=100, verbose_name='Autor')
    conference = models.CharField(max_length=100, verbose_name='Publicado en')
    description = models.TextField(verbose_name='Resumen')
    isbn = models.CharField(max_length=20, verbose_name='ISBN', default='')
    issn = models.CharField(max_length=20, verbose_name='ISSN', default='')
    publish_date = models.DateField(verbose_name='Fecha de Publicacion')
    created_at = models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')

    class Meta:
        verbose_name = 'Publicacion'
        verbose_name_plural = 'Publicaciones'
        ordering = ('id',)

    def __str__(self):
        return self.title
