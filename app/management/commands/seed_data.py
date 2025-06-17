import random
from django.core.management.base import BaseCommand
from app.models import Menu, MenuItem


class Command(BaseCommand):
    help = 'Заполняет меню test-данными с глубокой иерархией'

    def add_arguments(self, parser):
        parser.add_argument(
            '--menu_name',
            type=str,
            default='main_menu',
            help='Имя меню для заполнения'
        )
        parser.add_argument(
            '--total_items',
            type=int,
            default=100,
            help='Общее количество пунктов меню (примерно)'
        )
        parser.add_argument(
            '--max_depth',
            type=int,
            default=4,
            help='Максимальная глубина вложенности'
        )
        parser.add_argument(
            '--max_children',
            type=int,
            default=5,
            help='Максимальное число дочерних пунктов у одного родителя'
        )

    def handle(self, *args, **options):
        menu_name = options['menu_name']
        max_depth = options['max_depth']
        max_children = options['max_children']

        self.stdout.write(f'Начинаем создание меню "{menu_name}"')

        menu, created = Menu.objects.get_or_create(name=menu_name)
        menu.items.all().delete()

        levels = {0: []}
        order_counter = 0

        root_count = 3
        self.stdout.write(f'Создаём {root_count} корневых пунктов')

        for i in range(1, root_count + 1):
            order_counter += 1
            item = MenuItem.objects.create(
                menu=menu,
                title=f'Item {i}',
                url=f'/item-{i}/',
                order=order_counter,
                parent=None
            )
            levels[0].append(item)

        def create_children(parent_items, current_depth):
            nonlocal order_counter
            if current_depth >= max_depth:
                return

            levels[current_depth] = []
            for parent in parent_items:
                child_count = 3
                for c in range(1, child_count + 1):
                    order_counter += 1
                    title = f'{parent.title}.{c}'
                    url = f'{parent.url}{c}/'
                    child = MenuItem.objects.create(
                        menu=menu,
                        title=title,
                        url=url,
                        order=order_counter,
                        parent=parent
                    )
                    levels[current_depth].append(child)

            if levels[current_depth]:
                create_children(levels[current_depth], current_depth + 1)

        create_children(levels[0], 1)

        self.stdout.write(self.style.SUCCESS(f'Создано пунктов меню: {order_counter}'))
