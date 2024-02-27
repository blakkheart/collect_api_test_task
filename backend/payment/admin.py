from django.contrib import admin

from payment.models import Collect, Payment, CollectPayment, Reason


class CollectPaymentInline(admin.TabularInline):
    model = CollectPayment
    extra = 1


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    inlines = (
        CollectPaymentInline,
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass


@admin.register(Reason)
class ReasonAdmin(admin.ModelAdmin):
    pass
