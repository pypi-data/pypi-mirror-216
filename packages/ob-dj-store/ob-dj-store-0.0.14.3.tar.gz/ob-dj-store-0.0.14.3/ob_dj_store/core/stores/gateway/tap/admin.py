from django.contrib import admin

from ob_dj_store.core.stores.gateway.tap.models import TapPayment


class TapPaymentAdmin(admin.ModelAdmin):
    list_display = [
        "charge_id",
        "amount",
        "source",
        "status",
    ]
    list_filter = ("status", "source")
    search_fields = [
        "charge_id",
    ]

    def get_queryset(self, request):

        return (
            super()
            .get_queryset(request)
            .select_related(
                "payment__payment_tax",
            )
            .prefetch_related(
                "payment__orders__items", "payment__orders__shipping_method"
            )
        )


admin.site.register(TapPayment, TapPaymentAdmin)
