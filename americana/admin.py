from django.contrib import admin
from americana.models import Tesis, Publicacion

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
