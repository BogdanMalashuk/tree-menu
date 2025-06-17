from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    re_path(r'^(?P<slug>[-\w/]+)/$', menu_page, name='menu_page'),  # Обработка вложенных URL-пунктов меню.
]
