from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet,
                    TagViewSet, DownloadShoppingCart)

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
     path('recipes/download_shopping_cart/',
          DownloadShoppingCart.as_view(), name='download_shopping_cart'),
     path('', include(router.urls)),
]
