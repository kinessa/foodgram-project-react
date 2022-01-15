from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import RecipeFilter, IngredientSearchFilter
from .models import (Ingredient, Recipe, Tag, Favorite, IngredientInRecipe,
                     ShoppingCart)
from .pagination import CustomPageNumberPagination
from .permissions import AdminOrAuthorOrReadOnly
from .serializers import (IngredientSerializer, TagSerializer,
                          CreateRecipeSerializers, RecipesSerializers,
                          FavouriteRecipeSerializer, ShoppingCartSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    filter_backends = [IngredientSearchFilter]
    search_fields = ('^name', )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = RecipeFilter
    permission_classes = (AdminOrAuthorOrReadOnly,)
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipesSerializers
        return CreateRecipeSerializers

    def get_renderer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    @action(detail=True, permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = FavouriteRecipeSerializer(data=data,
                                               context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = ShoppingCartSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_cart = get_object_or_404(
            ShoppingCart, user=user, recipe=recipe
        )
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCart(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_shopping_cart = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user).values_list(
            'ingredient__name', 'amount', 'ingredient__measurement_unit')
        all_count_ingredients = user_shopping_cart.values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
            total=Sum('amount')).order_by('-total')
        ingredients_list = []
        for ingredient in all_count_ingredients:
            ingredients_list.append(
                f'{ingredient["ingredient__name"]} - '
                f'{ingredient["total"]} '
                f'{ingredient["ingredient__measurement_unit"]} \n'
            )
        return HttpResponse(ingredients_list, {
            'content_type': 'text/plain',
            'Content-Disposition': 'attachment; filename="shopping_list.txt"'
        })
