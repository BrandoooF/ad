from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile

# Register your models here.

UserAdmin.fieldsets += (
    ('FX Status', {'fields': ('profile_img', 'receives_emails', 'receives_emails_from_organizers')}),
)


class FxUserAdmin(UserAdmin):
    model = User

    def __str__(self):
        return self.username


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
