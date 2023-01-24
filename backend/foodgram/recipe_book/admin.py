from django.contrib import admin
from recipe_book.models import (Favorite, Ingredient, Recipe, Structure,
                                Subscription, Tag)


class RecipeIngredientInline(admin.StackedInline):
    model = Ingredient.recipe.through
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = ('name', 'author', 'count_is_favorites')
    ordering = ('name', 'author',)
    search_fields = ('author', 'name', 'tags')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'

    def count_is_favorites(self, obj):
        return obj.favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    ordering = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Tag)
admin.site.register(Structure)
admin.site.register(Subscription)
admin.site.register(Favorite)
