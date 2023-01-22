from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
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
    name = models.CharField(max_length=30, verbose_name='Тег', unique=True)
    color = models.CharField(max_length=16, unique=True, verbose_name='Цвет')
    slug = models.SlugField(unique=True, verbose_name='Адрес')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name[:15]


class Ingredient(models.Model):
    """Ингридиенты."""
    name = models.CharField(max_length=75,
                            unique=True,
                            verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=80,
        choices=UNITS,
        default='g',
        verbose_name='Единица измерения',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name[:15]


class Recipe(models.Model):
    """Рецепты."""
    author = models.ForeignKey(User,
                               related_name='recipes',
                               on_delete=models.CASCADE)
    name = models.CharField(max_length=200,
                            unique=True,
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
        related_name='recipe',
        blank=True,
        verbose_name='Ингридиенты',
        help_text='Ингридиенты, из которых состоит блюда',
        through='Structure',
    )
    tags = models.ManyToManyField(Tag)
    cooking_time = models.PositiveIntegerField(
        verbose_name="Время приготовления в минутах",
        validators=[MinValueValidator(1), MinValueValidator(600)]
    )

    class Meta:
        ordering = ('cooking_time',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:15]


class Structure(models.Model):
    """Состав рецептов"""
    recipe = models.ForeignKey(Recipe,
                               related_name='structure',
                               on_delete=models.CASCADE, )
    ingredients = models.ForeignKey(Ingredient,
                                    related_name='structure',
                                    on_delete=models.CASCADE, )
    amount = models.IntegerField(verbose_name='Количество',
                                 validators=[MinValueValidator(1),
                                             MinValueValidator(999)])

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Состав рецепта'
        verbose_name_plural = 'Составы рецепта'

    def __str__(self):
        return self.recipe.name[:15]


class Subscription(models.Model):
    """Подписки."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed',
        verbose_name='Автор'
    )

    class Meta:
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Favorite(models.Model):
    """Избранное."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipes'
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}: {self.recipe}'


class Shopping_cart(models.Model):
    """Корзина покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}: {self.recipe}'
