from django.contrib import admin
from .models import User, Tier, TierImage
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin


class UserAdmin(DefaultUserAdmin):
    fieldsets = (
        ('User', {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'tier')}),
    )
    list_display = (
        'username',
        'email',
        'tier',
    )


admin.site.register(User, UserAdmin)
admin.site.register(Tier)
admin.site.register(TierImage)
