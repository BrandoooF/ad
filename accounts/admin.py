from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserProfile

# Register your models here.


class FxUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_img',)}),
    )


admin.site.register(User, FxUserAdmin)
admin.site.register(UserProfile)
