from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy

from larp_egov.apps.accounts.models import UserAccount


admin.site.unregister(Group)


@admin.register(UserAccount)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {"fields": ("password",)}),
        (gettext_lazy("Personal info"), {"fields": ("email", "telegram_id",)}),
        (
            gettext_lazy("Ingame permissions"),
            {"fields": ("is_police", "is_security", "is_hacker",)},
        ),
        (
            gettext_lazy("Game related info"), 
            {"fields": ("first_name", "last_name", "character_id", "date_of_birth", "place_of_work", "bank_account", "defence_level")}
        ),
        (
            gettext_lazy("Comment fields"), 
            {"fields": ("police_comment_field", "security_comment_field",)}
        ),
        (gettext_lazy("Important dates"), {"fields": ("last_login", "date_joined")}),
        (
            gettext_lazy("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions", "is_verified")},
        ),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),)
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("first_name", "last_name", "email", "telegram_id", "character_id")
    ordering = ("email",)
    readonly_fields = ("telegram_id", "email", "character_id")
