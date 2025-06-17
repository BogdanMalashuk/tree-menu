from django.shortcuts import render
from .models import Menu, MenuItem
from django.core.exceptions import ObjectDoesNotExist
from typing import List, Dict, Any
from django.http import HttpRequest, HttpResponse, Http404


def build_menu_tree(menu_items: List[MenuItem]) -> List[Dict[str, Any]]:
    """
    Построить древовидную структуру меню из плоского списка пунктов.

    Аргументы:
        menu_items (List[MenuItem]): Список пунктов меню.

    Возвращает:
        List[Dict[str, Any]]: Список вложенных словарей, представляющих дерево меню.
    """
    menu_dict = {}
    tree = []

    for item in menu_items:
        item_dict = {
            'id': item.id,
            'title': item.title,
            'url': item.get_url(),
            'children': [],
            'active': False,
            'open': False,
        }
        menu_dict[item.id] = item_dict

    for item in menu_items:
        item_dict = menu_dict[item.id]
        if item.parent_id:
            parent = menu_dict[item.parent_id]
            parent['children'].append(item_dict)
        else:
            tree.append(item_dict)

    return tree


def home(request: HttpRequest) -> HttpResponse:
    """
    Представление главной страницы.

    Аргументы:
        request (HttpRequest): Объект HTTP-запроса.

    Возвращает:
        HttpResponse: Ответ с отрендеренным шаблоном главной страницы.
    """
    try:
        menu = Menu.objects.get(name='main_menu')
    except ObjectDoesNotExist:
        menu_items = []
    else:
        menu_items = MenuItem.objects.filter(menu=menu).select_related('parent')

    tree = build_menu_tree(menu_items)
    return render(request, 'main/home.html', {'menu': tree})


def menu_page(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Формирует полный путь с ведущим и завершающим слэшем, ищет пункт меню с совпадающим URL.

    Аргументы:
        request (HttpRequest): Объект HTTP-запроса.
        slug (str): Часть URL, например 'about/team'.

    Возвращает:
        HttpResponse: Ответ с отрендеренным шаблоном страницы меню.
    """
    path = '/' + slug.strip('/') + '/'
    menu_item = MenuItem.objects.filter(url=path).first()
    if not menu_item:
        raise Http404("Page not found in menu")

    return render(request, 'menus/page.html', {'menu_item': menu_item})
