from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

UNITS = (
    ('g', 'г'),
    ('glass', 'стакан'),
    ('as_your_taste', 'по вкусу'),
    ('big_spoon', 'ст. л.'),
    ('pc', 'шт.'),
    ('ml', 'мл'),
    ('little_cpoon', 'ч. л.'),
    ('drop', 'капля'),
    ('asterisk', 'звездочка'),
    ('pinch', 'щепотка'),
    ('handful', 'горсть'),
    ('piece', 'кусок'),
    ('kg', 'кг'),
    ('package', 'пакет'),
    ('bundle', 'пучок'),
    ('slice', 'долька'),
    ('pot', 'банка'),
    ('packing', 'упаковка'),
    ('tooth', 'зубчик'),
    ('layer', 'пласт'),
    ('pack', 'пачка'),
    ('carcass', 'тушка'),
    ('pod', 'стручок'),
    ('twig', 'веточка'),
    ('bottle', 'бутылка'),
    ('l', 'л'),
    ('loaf', 'батон'),
    ('bag', 'пакетик'),
    ('leaf', 'лист'),
    ('stem', 'стебель'),
)


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


class Ingredient(models.Model):
    """Ингридиенты."""
    name = models.CharField(max_length=75, unique=True,
                            verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=80, choices=UNITS, default='g',
        verbose_name='Единица измерения',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name[:15]


class Recipe(models.Model):
    """Рецепт."""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True,
                            verbose_name='Название')
    image = models.ImageField(
        upload_to=directory_path,
        null=True,
        default=None,
    )
    text = models.CharField(max_length=500,
                            null=True,
                            blank=True,
                            verbose_name='Краткое описание рецепта '
                                         '(макс 500 символов)')
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='reciepe',
        blank=True,
        verbose_name='Ингридиенты',
        help_text='Ингридиенты, из которых состоит блюда',
        through='Structure',
    )
    tags = models.ManyToManyField(Tag)
    cooking_time = models.PositiveIntegerField(
        verbose_name="Время приготовления в минутах", )

    class Meta:
        ordering = ('cooking_time',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:15]


class Structure(models.Model):
    """Состав рецептов"""
    recipe = models.ForeignKey(Recipe, related_name='structure',
                               on_delete=models.CASCADE, )
    ingredients = models.ForeignKey(Ingredient, related_name='structure',
                                    on_delete=models.CASCADE, )
    amount = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Состав рецепта'
        verbose_name_plural = 'Составы рецепта'

    def __str__(self):
        return self.recipe.name[:15]
