from django.db import models
from django.urls import reverse, NoReverseMatch


class Menu(models.Model):
    """
    Модель меню, которое может содержать множество пунктов (MenuItem).
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """
    Пункт меню, может быть частью другого пункта (рекурсивная структура).
    Поддерживает как прямой URL, так и именованный путь Django.
    """
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)
    named_url = models.CharField(max_length=100, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_url(self):
        """
        Возвращает актуальный URL пункта меню.
        Приоритет: сначала именованный маршрут (named_url), затем прямой url.
        Если именованный маршрут не найден, возвращается исходная строка.
        """
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return self.named_url
        return self.url
