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
            {
                "fields": (
                    "is_police",
                    "is_security",
                    "is_hacker",
                )
            },
        ),
        (
            gettext_lazy("Game related info"),
            {"fields": (
                "first_name",
                "last_name",
                "character_id",
                "date_of_birth",
                "place_of_work",
                "bank_account",
                "defence_level",
                "system_heat",
                "has_special_hack_value",
                "special_hack_pro_price",
                "is_warned_of_hack_attack",
                "custom_special_hack_text_field",
                "custom_hack_beginning_text_field",
            )}
        ),
        (
            gettext_lazy("Comment fields"), 
            {"fields": ("police_comment_field", "security_comment_field",)}
        ),
        (
            gettext_lazy("Permissions"),
            {"fields": (
                "is_active", "is_staff", "is_superuser", 'is_service_account', 'is_corporate_fiction_account', "is_fiction_account",
                "requests_made_since_last_purge",
            )},
        ),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),)
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active", 'character_id', "bank_account")
    search_fields = ("first_name", "last_name", "email", "telegram_id", "character_id")
    ordering = ("email",)
    readonly_fields = ("character_id",)
