"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser'
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser'
            )
        }),
    )


class DrillScoreAdmin(admin.ModelAdmin):
    """Define the admin pages for drill scores."""
    ordering = ['id']
    list_display = ['user', 'drill', 'score', 'maxScore']
    search_fields = ['user', 'drill']
    list_filter = ['user', 'drill']


class DrillAdmin(admin.ModelAdmin):
    """Define the admin pages for drills."""
    ordering = ['id']
    list_display = ['uploadedBy', 'name', 'type']
    search_fields = ['uploadedBy', 'name', 'type']
    list_filter = ['uploadedBy', 'type']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.DrillScore, DrillScoreAdmin)
admin.site.register(models.Drill, DrillAdmin)
