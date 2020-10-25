from django.contrib import admin
from larp_egov.apps.law_enforcement.models import MisconductType, MisconductReport


class MisconductTypeAdmin(admin.ModelAdmin):
    list_display = ['title', 'misconduct_code', 'suggested_penalty']
    list_editable = ['misconduct_code', 'suggested_penalty']
    search_fields = ['title', 'misconduct_code']
    readonly_fields = ['uuid', 'created', 'updated']


class MisconductReportAdmin(admin.ModelAdmin):
    list_display = ['reporter', 'reported_person', 'officer_in_charge', 'misconduct_type', 'uuid']
    list_filter = ['reporter', 'reported_person', 'officer_in_charge', 'misconduct_type']
    readonly_fields = ['uuid', 'created', 'updated']

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related(
            'reporter',
            'reported_person',
            'officer_in_charge',
            'misconduct_type'
        )


admin.site.register(MisconductType, MisconductTypeAdmin)
admin.site.register(MisconductReport, MisconductReportAdmin)
