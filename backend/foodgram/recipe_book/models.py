from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

UNITS = [
    ('mm', 'мм'),
    ('cm', 'см'),
    ('dm', 'дм'),
    ('m', 'м'),
    ('in', 'дюйм'),
    ('ft', 'фут'),
    ('yd', 'ярд'),
    ('I; L; dm^3', 'л; дм^3'),
    ('m^3', 'м^3'),
    ('dl', 'дл'),
    ('hl', 'гл'),
    ('hg', 'гг'),
    ('mg', 'мг'),
    ('МС', 'кар'),
    ('g', 'г'),
    ('kg', 'кг'),
    ('t', 'т'),
    ('pack', 'упак'),
    ('pc', 'шт'),
    ('box', 'ящ'),
    ('set', 'компл'),
    ('bot', 'бут'),

]


def directory_path(instance, filename):
    """Функция определяющая путь к сохраняемому файлу"""
    return f'reciepts/{instance.name}/{filename}'


class Tag(models.Model):
    """Теги."""
    name = models.CharField(max_length=30, verbose_name='Тег')
    color = models.CharField(max_length=16)
    slug = models.SlugField(unique=True, verbose_name='Адрес')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name[:15]


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True,
                            verbose_name='Название')
    image = models.ImageField(
        upload_to=directory_path,
        null=True,
        default=None
    )
    description = models.CharField(max_length=500,
                                   null=True,
                                   blank=True,
                                   verbose_name='Краткое описание рецепта '
                                                '(макс 500 символов)')
    tags = models.ManyToManyField(Tag)
    cooking_time = models.DurationField(null=True, blank=True)

    class Meta:
        ordering = ('cooking_time',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ингридиенты"""
    name = models.CharField(max_length=75, unique=True,
                            verbose_name='Название')
    quantity = models.IntegerField(verbose_name="Количество")
    unit_of_measurement = models.CharField(
        max_length=80, choices=UNITS, default='KG',
        verbose_name='Единица измерения',
    )
