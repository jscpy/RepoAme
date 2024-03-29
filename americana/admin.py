from django.contrib import admin
from americana.models import Tesis, Publicacion, Constancia, Area


@admin.register(Tesis)
class TesisModelAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'autor', 'program', 'publish_date'
    )


@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'autor', 'conference', 'description',
        'area', 'isbn', 'issn', 'publish_date'
    )


@admin.register(Constancia)
class ConstanciaAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'autor', 'area', 'director',
        'conference', 'publish_date'
    )


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = (
        'name', 'slug',
    )
