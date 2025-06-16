from django import template
from app.models import MenuItem
from collections import defaultdict

register = template.Library()


@register.inclusion_tag('menus/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    current_url = context['request'].path
    all_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')

    # Группируем по parent_id
    children_map = defaultdict(list)
    item_map = {}

    for item in all_items:
        item_map[item.id] = item
        children_map[item.parent_id].append(item)

    def build_tree(parent_id=None, active_path=None):
        items = []
        for item in children_map.get(parent_id, []):
            item_url = item.get_absolute_url()
            is_active = (item_url == current_url)
            children = build_tree(item.id, active_path)
            items.append({
                'item': item,
                'children': children,
                'is_active': is_active or any(child['is_active'] for child in children),
            })
        return items

    tree = build_tree()
    return {'menu_tree': tree}
