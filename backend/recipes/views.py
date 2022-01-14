import django_filters.rest_framework
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import RecipeFilter, IngredientSearchFilter
from .models import (Ingredient, Recipe, Tag, Favorite, IngredientInRecipe, ShoppingCart)
from .pagination import CustomPageNumberPagination
from .permissions import AdminOrAuthorOrReadOnly
from .serializers import (IngredientSerializer, TagSerializer, UserSerializer, CreateRecipeSerializers,
                          RecipesSerializers, FavouriteRecipeSerializer, ShoppingCartSerializer)


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
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_class = RecipeFilter
    permission_classes = [AdminOrAuthorOrReadOnly, ]
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipesSerializers
        return CreateRecipeSerializers

    def get_renderer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class FavouriteViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            return Response('Рецепт уже в избранном',
                            status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.create(user=user, recipe=recipe)
        serializer = FavouriteRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        favorite_obj = get_object_or_404(Favorite, user=user, recipe=recipe)
        if not favorite_obj:
            return Response('Рецепт не был в избранном',
                            status=status.HTTP_400_BAD_REQUEST)
        favorite_obj.delete()
        return Response('Удалено', status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            return Response('Рецепт уже добавлен',
                            status=status.HTTP_400_BAD_REQUEST)
        ShoppingCart.objects.create(user=user, recipe=recipe)
        serializer = ShoppingCartSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        shopping_list_obj = get_object_or_404(ShoppingCart, user=user,
                                              recipe=recipe)
        if not shopping_list_obj:
            return Response('Рецепта нет в списке покупок',
                            status=status.HTTP_400_BAD_REQUEST)
        shopping_list_obj.delete()
        return Response('Удалено', status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCart(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        shopping_cart = user.shopping_cart.all()
        buying_list = {}
        for record in shopping_cart:
            recipe = record.recipe
            ingredients = IngredientInRecipe.objects.filter(recipe=recipe)
            for ingredient in ingredients:
                amount = ingredient.amount
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                if name not in buying_list:
                    buying_list[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount
                    }
                else:
                    buying_list[name]['amount'] = (buying_list[name]['amount']
                                                   + amount)

        wishlist = []
        for item in buying_list:
            wishlist.append(f'{item} - {buying_list[item]["amount"]} '
                            f'{buying_list[item]["measurement_unit"]} \n')
        wishlist.append('\n')
        wishlist.append('FoodGram, 2022')
        response = HttpResponse(wishlist, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="wishlist.txt"'
        return response
