from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from americana.models import Tesis, Profile, Publicacion

admin.site.unregister(User)

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'get_fullname', 'conference', 'description', 'publish_date'
    )

    def get_fullname(self, obj):
        return obj.student.get_full_name()

    get_fullname.short_description = 'Alumno'
    get_fullname.admin_order_field = 'first_name'

@admin.register(Tesis)
class TesisModelAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'get_fullname', 'program', 'publish_date'
    )
    
    def get_fullname(self, obj):
        return obj.autor.get_full_name()

    get_fullname.short_description = 'Autor'
    get_fullname.admin_order_field = 'first_name'

class ProfileInline(admin.StackedInline):
    model = Profile
    verbose_name_plural = 'Perfil'
    fk_name = 'user'

@admin.register(User)
class UserProfileAdmin(UserAdmin):
    inlines = (ProfileInline, )
