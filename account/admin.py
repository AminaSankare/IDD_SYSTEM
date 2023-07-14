from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name',
                    'gender', 'is_active', 'last_login', 'image',)
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_registrar', 'is_superuser', 'is_active')
    fieldsets = (
        ('User Credential', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name',
         'gender', 'phone1', 'phone2', ('profilePicture',),)}),
        ('Permissions', {'fields': ('is_active',
         'is_staff', 'is_registrar', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        ('New User', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'gender', 'phone1', 'phone2', ('profilePicture',),),
        }),
        ('Permission', {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_registrar', 'is_superuser',),
        }),
        ('User Credential', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
    )
    ordering = ('email',)


admin.site.unregister(Group)
