# Generated by Django 4.1.5 on 2023-01-12 21:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipe_book', '0005_rename_description_recipe_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(choices=[('g', 'г'), ('glass', 'стакан'), ('as_your_taste', 'по вкусу'), ('big_spoon', 'ст. л.'), ('pc', 'шт.'), ('ml', 'мл'), ('little_cpoon', 'ч. л.'), ('drop', 'капля'), ('asterisk', 'звездочка'), ('pinch', 'щепотка'), ('handful', 'горсть'), ('piece', 'кусок'), ('kg', 'кг'), ('package', 'пакет'), ('bundle', 'пучок'), ('slice', 'долька'), ('pot', 'банка'), ('packing', 'упаковка'), ('tooth', 'зубчик'), ('layer', 'пласт'), ('pack', 'пачка'), ('carcass', 'тушка'), ('pod', 'стручок'), ('twig', 'веточка'), ('bottle', 'бутылка'), ('l', 'л'), ('loaf', 'батон'), ('bag', 'пакетик'), ('leaf', 'лист'), ('stem', 'стебель')], default='g', max_length=80, verbose_name='Единица измерения'),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribed', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique_subscription'),
        ),
    ]