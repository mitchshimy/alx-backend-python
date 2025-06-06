from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Conversation, Message

# Optional: Customize how the User model appears in the admin
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('user_id', 'username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('user_id',)

admin.site.register(User, UserAdmin)
admin.site.register(Conversation)
admin.site.register(Message)
