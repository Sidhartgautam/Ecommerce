from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Custom User Admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Fields to display in the user list
    list_display = ['username', 'email', 'phone', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'email', 'phone']
    ordering = ['username']

    # Fieldsets for user detail page
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields for the add/edit user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'phone', 'address', 'profile_picture', 'is_active', 'is_staff')
        }),
    )

    # Make fields read-only (if needed)
    readonly_fields = ['last_login', 'date_joined']

    # Function to display profile picture in the list view
    def profile_picture_thumbnail(self, obj):
        if obj.profile_picture:
            return f'<img src="{obj.profile_picture.url}" style="width: 40px; height: 40px; border-radius: 50%;">'
        return "No Image"

    profile_picture_thumbnail.short_description = "Profile Picture"
    profile_picture_thumbnail.allow_tags = True
