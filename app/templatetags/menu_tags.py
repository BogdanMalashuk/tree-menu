from django import template
from app.models import MenuItem
from collections import defaultdict

register = template.Library()


@register.inclusion_tag('menus/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    current_path = context['request'].path
    items = (
        MenuItem.objects
        .filter(menu__name=menu_name)
        .select_related('parent')
        .order_by('order')
    )

    children_map = defaultdict(list)

    for item in items:
        item.url = item.get_url()
        item.active = False
        item.open = False
        if item.parent_id:
            children_map[item.parent_id].append(item)

    for item in items:
        item.child_nodes = children_map.get(item.id, [])

    def mark_active_branch(item):
        if item.url == current_path:
            item.active = True
            return True
        for child in getattr(item, 'child_nodes', []):
            if mark_active_branch(child):
                item.open = True
                return True
        return False

    root_items = [item for item in items if item.parent is None]
    for item in root_items:
        mark_active_branch(item)

    return {'menu': root_items}
