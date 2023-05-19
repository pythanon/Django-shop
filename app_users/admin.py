from django.contrib import admin

from app_users.models import Profile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["username", "full_name", "phone", "email", "avatar"]
    search_fields = ["username", "full_name", "phone", "email"]


admin.site.register(Profile, UserProfileAdmin)
