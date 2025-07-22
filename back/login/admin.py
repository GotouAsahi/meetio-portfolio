from django.contrib import admin

# Register your models here.
from .models import User
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "id")
    list_filter = ("date_joined",)
admin.site.register(User,UserAdmin)