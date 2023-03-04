from django.contrib import admin
from .models import User, Tier, TierImage

admin.site.register(User)
admin.site.register(Tier)
admin.site.register(TierImage)
