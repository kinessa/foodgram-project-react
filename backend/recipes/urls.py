from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                    ShoppingCartViewSet, DownloadShoppingCart, FavouriteViewSet)

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
     path('', include(router.urls)),
     # path('recipes/<int:recipe_id>/favorite/',
     #      FavouriteViewSet.as_view(), name='add_recipe_to_favorite'),
     # path('recipes/<int:recipe_id>/shopping_cart/',
     #      ShoppingCartViewSet.as_view(), name='is_shopping_cart'),
     # path('recipes/download_shopping_cart/',
     #      DownloadShoppingCart.as_view(), name='download_shopping_cart')
]
