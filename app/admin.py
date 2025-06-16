from django.contrib import admin
from .models import MenuItem, Menu


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'parent', 'order')
    list_filter = ('menu',)
    ordering = ('menu', 'parent__id', 'order')


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name']
