from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Specify the fields to display in the admin list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')

    # Add filtering options in the admin panel
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')

    # Define fields for the user edit page
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),  # Add the custom user_type field
    )

    # Define fields for the user creation page
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type',)}),
    )

    # Fields to search for in the admin panel
    search_fields = ('username', 'email', 'user_type')

    # Define ordering
    ordering = ('username',)

# Register the CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
