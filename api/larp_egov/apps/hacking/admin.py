from django.contrib import admin
from larp_egov.apps.hacking.models import HackingSession


class HackingSessionAdmin(admin.ModelAdmin):
    list_display = ['hacker', 'target', 'ticks_remaining', 'is_active',]
    list_filter = ['hacker', 'target', 'is_active']
    readonly_fields = ['uuid', 'created', 'updated']

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related(
            'hacker',
            'target',
        )


admin.site.register(HackingSession, HackingSessionAdmin)
