from django.db import migrations

INITIAL_TAGS = [
    {'color': 'orange', 'name': 'Завтрак', 'slug': 'breakfast'},
    {'color': 'green', 'name': 'Обед', 'slug': 'lunch'},
    {'color': 'purple', 'name': 'Ужин', 'slug': 'dinner'}
]


def add_tags(apps, schema_editor):
    Tag = apps.get_model('recipe_book', 'Tag')
    for tag in INITIAL_TAGS:
        new_tag = Tag(**tag)
        new_tag.save()


def remove_tags(apps, schema_editor):
    Tag = apps.get_model('recipe_book', 'Tag')
    for tag in INITIAL_TAGS:
        Tag.objects.get(name=tag['name']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_book', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(
            add_tags,
            remove_tags,
        )
    ]
