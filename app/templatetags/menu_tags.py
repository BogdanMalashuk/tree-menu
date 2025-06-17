from django import template
from app.models import MenuItem
from collections import defaultdict

register = template.Library()


@register.inclusion_tag('menus/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    """
    Кастомный тег Django template для отрисовки иерархического меню с подсветкой активного пункта и раскрытием активной ветки.

    :param context: контекст шаблона, включающий request для получения текущего URL
    :param menu_name: имя меню, которое нужно отобразить
    :return: словарь с иерархией меню для шаблона menus/menu.html
    """
    current_path = context['request'].path

    # Получаем все пункты меню указанного имени, сразу подтягиваем parent
    items = (
        MenuItem.objects
        .filter(menu__name=menu_name)
        .select_related('parent')
        .order_by('order')
    )

    # Словарь, группирующий дочерние элементы по ID родителя
    children_map = defaultdict(list)

    for item in items:
        item.url = item.get_url()
        item.active = False
        item.open = False
        if item.parent_id:
            children_map[item.parent_id].append(item)

    # Назначаем каждому элементу список его дочерних пунктов
    for item in items:
        item.child_nodes = children_map.get(item.id, [])

    def mark_active_branch(item):
        """
        Рекурсивно помечает активные пункты меню и все родительские ветки как открытые.
        :param item: пункт меню
        :return: True, если в ветке найден активный элемент
        """
        if item.url == current_path:
            item.active = True
            return True
        for child in getattr(item, 'child_nodes', []):
            if mark_active_branch(child):
                item.open = True  # Раскрываем родителя, если активен хотя бы один потомок
                return True
        return False

    root_items = [item for item in items if item.parent is None]

    for item in root_items:
        mark_active_branch(item)

    return {'menu': root_items}
