import json

from django.db import migrations
from django.db import transaction

from foodgram.settings import BASE_DIR

with open(str(BASE_DIR) + '/fixtures/ingredients.json', encoding='utf-8') as f:
    INITIAL_INGRIDIENTS = json.load(f)


def add_ingredients(apps, schema_editor):
    Ingredient = apps.get_model('recipe_book', 'Ingredient')
    for ingredient in INITIAL_INGRIDIENTS:
        try:
            with transaction.atomic():
                new_ingredient = Ingredient(**ingredient)
                new_ingredient.save()
        except Exception as e:
            print(f'Ошибка с {ingredient},текст ошибки:{e}')



def remove_ingredients(apps, schema_editor):
    Ingredient = apps.get_model('recipe_book', 'Ingredient')
    for ingredient in INITIAL_INGRIDIENTS:
        Ingredient.objects.get(name=ingredient['name']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('recipe_book', '0003_add_tags'),
    ]

    operations = [
        migrations.RunPython(
            add_ingredients,
            remove_ingredients,
        )
    ]
