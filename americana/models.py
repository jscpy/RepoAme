from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.db import models


class Autor(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.slug:
            fullname = f'{self.first_name} {self.last_name}'
            self.slug = slugify(fullname)
        return super().save(*args, **kwargs)


class Area(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre del Area')
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tesis(models.Model):
    PROGRAMAS = (
        ('Maestria', 'Maestria',),
        ('Doctorado', 'Doctorado',),
    )

    file = models.FileField(upload_to='docs/tesis/', verbose_name='Documento', max_length=200)
    title = models.CharField(max_length=100, verbose_name='Titulo')
    autor = models.ForeignKey(Autor, verbose_name='Autor', related_name='tesis', on_delete=models.CASCADE)
    program = models.CharField(max_length=100, choices=PROGRAMAS, verbose_name='Programa')
    area = models.ForeignKey(Area, verbose_name='Area', related_name='tesis', on_delete=models.CASCADE)
    director = models.CharField(max_length=100, verbose_name='Director')
    co_director = models.CharField(max_length=100, verbose_name='Co-director')
    publish_date = models.DateField(verbose_name='Fecha de Publicacion')
    description = models.TextField(verbose_name='Resumen')
    created_at = models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')
    slug = models.SlugField()

    class Meta:
        verbose_name = 'Tesis'
        verbose_name_plural = 'Tesis'
        ordering = ('-id', )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def format_publish(self):
        return f"{self.title} ({self.publish_date.year})"


class Publicacion(models.Model):
    file = models.FileField(upload_to='docs/publicaciones/', verbose_name='Documento', max_length=200)
    title = models.CharField(max_length=100, verbose_name='Titulo')
    autor = models.ForeignKey(Autor, verbose_name='Autor', related_name='publicacion', on_delete=models.CASCADE)
    conference = models.CharField(max_length=100, verbose_name='Publicado en')
    description = models.TextField(verbose_name='Resumen')
    area = models.ForeignKey(Area, verbose_name='Area', related_name='publicacion', on_delete=models.CASCADE)
    isbn = models.CharField(max_length=20, verbose_name='ISBN', default='', null=True, blank=True)
    issn = models.CharField(max_length=20, verbose_name='ISSN', default='', null=True, blank=True)
    publish_date = models.DateField(verbose_name='Fecha de Publicacion')
    created_at = models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')
    slug = models.SlugField()

    class Meta:
        verbose_name = 'Publicacion'
        verbose_name_plural = 'Publicaciones'
        ordering = ('-id', )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def format_publish(self):
        return f"{self.title} ({self.publish_date.year})"


class Constancia(models.Model):
    file = models.FileField(upload_to='docs/constancia/', verbose_name='Documento', max_length=200)
    title = models.CharField(max_length=100, verbose_name='Titulo')
    autor = models.ForeignKey(Autor, verbose_name='Autor', related_name='constancia', on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Resumen')
    area = models.ForeignKey(Area, verbose_name='Area', related_name='constancia', on_delete=models.CASCADE)
    publish_date = models.DateField(verbose_name='Fecha de Publicacion')
    created_at = models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')
    slug = models.SlugField()

    class Meta:
        ordering = ('-id', )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def format_publish(self):
        return f"{self.title} ({self.publish_date.year})"
