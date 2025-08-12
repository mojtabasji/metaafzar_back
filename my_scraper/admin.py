from django.contrib import admin
from .models import User, IGPage

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff')
    ordering = ('-id',)
    readonly_fields = ('date_joined',)

@admin.register(IGPage)
class IGPageAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
    search_fields = ('username', 'followers', 'following', 'posts')
    list_filter = ('followers', 'following', 'posts')
    ordering = ('-id',)
    readonly_fields = ('date_scraped',)