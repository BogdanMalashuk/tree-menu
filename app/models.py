from django.db import models
from django.urls import reverse


class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    named_url = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=100)

    def get_absolute_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except:
                return "#"
        return self.url or "#"

    def __str__(self):
        return self.title
