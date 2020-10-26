from django.contrib import admin
from larp_egov.apps.banking.models import (
    BankTransaction,
    BankSubscription,
    BankUserSubscriptionIntermediary,
    Corporation,
    CorporationMembership,
)


class BankTransactionAdmin(admin.ModelAdmin):
    list_display = ['sender', 'reciever', 'amount', 'is_finished', 'is_cancelled',]
    list_filter = ['sender', 'reciever', 'is_cancelled', 'is_finished']
    readonly_fields = ['uuid', 'created', 'updated']


class BankUserSubscriptionIntermediaryInline(admin.StackedInline):
    model = BankUserSubscriptionIntermediary
    fields = ['subscriber', 'is_approved']


class BankSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'is_governmental_tax', 'extraction_period', 'limited_approval',]
    list_filter = ['is_governmental_tax', 'extraction_period', 'limited_approval',]
    readonly_fields = ['uuid', 'created', 'updated']
    inlines = [BankUserSubscriptionIntermediaryInline, ]


class CorporationMembershipInline(admin.StackedInline):
    model = CorporationMembership
    fields = ['member', 'status']


class CorporationAdmin(admin.ModelAdmin):
    list_display = ['title', 'corporation_bank_account', 'corporation_id']
    inlines = [CorporationMembershipInline, ]
    readonly_fields = ['uuid', 'created', 'updated']

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related(
            'linked_account',
        )
        return qs


admin.site.register(Corporation, CorporationAdmin)
admin.site.register(BankSubscription, BankSubscriptionAdmin)
admin.site.register(BankTransaction, BankTransactionAdmin)
