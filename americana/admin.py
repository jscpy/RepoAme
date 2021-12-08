from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from americana.models import Tesis, Profile, Congreso

admin.site.register(Congreso)
admin.site.unregister(User)

@admin.register(Tesis)
class TesisModelAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'get_fullname', 'program', 'publish'
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
