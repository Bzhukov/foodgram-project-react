# Generated by Django 4.1.5 on 2023-01-12 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_book', '0002_alter_ingredient_options_remove_ingredient_quantity_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='structure',
            old_name='ingridients',
            new_name='ingredients',
        ),
    ]
