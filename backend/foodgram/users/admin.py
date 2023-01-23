from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_editable = ('first_name', 'last_name', 'email',)
    ordering = ('first_name', 'last_name',)
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('email', 'first_name', 'last_name')
    empty_value_display = '-пусто-'


admin.site.register(User, CustomUserAdmin)
