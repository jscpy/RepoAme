from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def user_directory_path(instance, filename):
    if hasattr(instance, 'autor'):
        return f'docs/{instance.autor.username}/tesis/{filename}'
    elif hasattr(instance, 'student'):
        return f'docs/{instance.student.username}/congresos/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name="Usuario", on_delete=models.CASCADE)
    cellphone = models.CharField(max_length=10, verbose_name='Telefono', blank=True)
    career = models.CharField(max_length=100, verbose_name='Carrera', blank=True)
    year_graduate = models.CharField(max_length=4, verbose_name='Año de Terminación', blank=True)
    facebook = models.CharField(max_length=100, verbose_name='Facebook', blank=True)
    twitter = models.CharField(max_length=100, verbose_name='Twitter', blank=True)
    
    def __str__(self):
        return f'{self.user}'
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'


class Tesis(models.Model):
    
    PROGRAMAS = (
        ('Maestria', 'Maestria',),
        ('Doctorado', 'Doctorado',),
    )
    
    file = models.FileField(
        upload_to=user_directory_path, verbose_name='Documento')
    title = models.CharField(max_length=100, verbose_name='Titulo')
    autor = models.ForeignKey(User, verbose_name='Autor', related_name='tesis', on_delete=models.CASCADE)
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
    file = models.FileField(
        upload_to=user_directory_path, verbose_name='Documento')
    title = models.CharField(max_length=100, verbose_name='Titulo')
    student = models.ForeignKey(User, verbose_name='Alumno', related_name='congreso', on_delete=models.CASCADE)
    conference = models.CharField(max_length=100, verbose_name='Publicado en')
    description = models.TextField(verbose_name='Resumen')
    publish_date = models.DateField(verbose_name='Fecha de Publicacion')
    created_at = models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')

    class Meta:
        verbose_name = "Publicacion"
        verbose_name_plural = "Publicaciones"
        ordering = ('id',)

    def __str__(self):
        return self.conference


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
