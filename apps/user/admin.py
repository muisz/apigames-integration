from django.contrib import admin

from apps.user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'date_joined')
    search_fields = ('first_name', 'last_name')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        password = request.POST.get('password')
        if 'pbkdf2_sha256' not in password:
            obj.refresh_from_db()
            obj.set_password(password)
            obj.save()
