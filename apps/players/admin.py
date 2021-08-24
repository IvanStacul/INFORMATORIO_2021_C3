# Django
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

# Models
from django.contrib.auth.models import User
from .models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'picture')
    list_display_links = ('pk', 'user',)


class PlayerInline(admin.StackedInline):
    model = Player
    can_delete = False
    verbose_name_plural = 'players'


class UserAdmin(BaseUserAdmin):
    inlines = (PlayerInline,)
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff'
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
