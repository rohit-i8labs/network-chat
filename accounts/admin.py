from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'current_var_id', 'current_restaurant', 'user_token_expiry')
    list_filter = ('user_type',)
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = (
        ('User Information', {'fields': ('username', 'email', 'password')}),
        ('Custom Attributes', {'fields': ('user_type', 'user_token_expiry', 'current_var_id', 'current_restaurant')}),
    )
