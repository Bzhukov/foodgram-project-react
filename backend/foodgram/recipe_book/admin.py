from django.contrib import admin

from recipe_book.models import (Recipe, Ingredient, Tag, Structure,
                                Subscription, Favorite)

admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Structure)
admin.site.register(Subscription)
admin.site.register(Favorite)
