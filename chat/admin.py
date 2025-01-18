from django.contrib import admin
from .models import Restaurant, Offer, Message

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'total_customers', 'date_created', 'avg_stay_time', 'var_id')
    list_filter = ('date_created', 'qr_gen_frequency')
    search_fields = ('name', 'owner__username')
    ordering = ('date_created',)
    fieldsets = (
        ('Basic Information', {'fields': ('name', 'description', 'logo', 'owner', 'todays_special')}),
        ('Stats and Metrics', {'fields': ('total_customers', 'total_messages', 'total_qr_scanned')}),
        ('QR Settings', {'fields': ('var_id', 'qr_gen_frequency')}),
    )


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('description', 'time_based', 'duration')
    list_filter = ('time_based',)
    search_fields = ('description',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'timestamp', 'sender', 'is_private', 'receiver', 'restaurant')
    list_filter = ('timestamp', 'is_private')
    search_fields = ('text', 'sender__username', 'receiver__username', 'restaurant__name')
