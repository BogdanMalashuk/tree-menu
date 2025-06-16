from django.contrib import admin
from .models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu_name', 'parent', 'named_url', 'url')
    list_filter = ('menu_name',)