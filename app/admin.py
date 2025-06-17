from django.contrib import admin
from .models import MenuItem, Menu


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'parent', 'order')  # Колонки в списке
    list_filter = ('menu',)  # Фильтр по меню справа
    ordering = ('menu', 'parent__id', 'order')  # Сортировка по меню, затем по родителю и порядку


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name']  # Отображение имени меню
