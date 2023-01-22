from django.contrib import admin

from recipe_book.models import (Recipe, Ingredient, Tag, Structure,
                                Subscription, Favorite)


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Structure)
admin.site.register(Subscription)
admin.site.register(Favorite)

class RecipeIngredientInline(admin.StackedInline):
    model = Ingredient.recipe.through
    min_num = 1


@admin.register(Recipe)
class IngredientAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)