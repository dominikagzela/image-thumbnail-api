from django.contrib import admin
from .models import User, Tier, TierImage
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin


class UserAdmin(DefaultUserAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Tier)
admin.site.register(TierImage)
