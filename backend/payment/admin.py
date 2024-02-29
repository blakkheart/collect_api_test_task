from django.contrib import admin

from payment.models import Collect, CollectPayment, Payment, Reason


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'title',
        'reasons',
        'amount_to_collect',
        'amount_collected',
        'amount_of_people_donated',
        'end_datetime',
        'created_at',
    )
    readonly_fields = (
        'amount_collected',
        'amount_of_people_donated',
        'created_at'
    )
    list_filter = (
        'amount_to_collect',
        'reasons',
        'created_at',
        'end_datetime'
    )
    search_fields = (
        'title',
        'author',
    )
    list_per_page = 25

    def get_queryset(self, request):
        queryset = super(CollectAdmin, self).get_queryset(request)
        queryset = queryset.prefetch_related(
            'payments').select_related('author', 'reasons')
        return queryset


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'amount',
        'donated_at',
        'invisible',
        'first_name_user',
        'last_name_user',
        'email_user',
    )
    readonly_fields = (
        'amount',
        'donated_at',
    )
    list_filter = (
        'amount',
        'donated_at',
        'invisible',
        'email_user'
    )
    search_fields = (
        'email_user',
    )
    list_per_page = 25


@admin.register(Reason)
class ReasonAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )
    list_filter = (
        'title',
    )
    search_fields = (
        'title',
    )
    list_per_page = 25


@admin.register(CollectPayment)
class CollectPaymentAdmin(admin.ModelAdmin):
    list_display = (
        'collect',
        'payment',
    )
    list_filter = (
        'collect',
        'payment',
    )
    search_fields = (
        'collect',
        'payment',
    )
    list_select_related = (
        'collect',
        'payment',
    )
    list_per_page = 25


admin.site.site_header = 'Администрирование Сбор денег'
admin.site.index_title = 'Администрирование сайта Сбор денег'
admin.site.empty_value_display = 'Не задано'
