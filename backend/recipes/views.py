import django_filters.rest_framework
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import RecipeFilter
from .models import (Ingredient, Recipe, Tag, CustomUser, Follow)
from .permissions import AdminOrAuthorOrReadOnly
from .serializers import (IngredientSerializer, TagSerializer, RecipeSerializer, ListRecipeSerializers,
                          UserSerializer, CreateRecipeSerializers)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_class = RecipeFilter
    permission_classes = [AdminOrAuthorOrReadOnly, ]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ListRecipeSerializers
        return CreateRecipeSerializers

    def get_renderer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class FollowViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        user = request.user
        author = get_object_or_404(CustomUser, id=user_id)
        if Follow.objects.filter(user=user, id=user_id):
            return Response('Уже подписаны', status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.create(user=user, author=author)
        serializer = UserSerializer(author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        user = request.user
        author = get_object_or_404(CustomUser, id=user_id)
        try:
            follow = get_object_or_404(user=user, author=author)
            follow.delete()
            return Response('Удалено', status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response('Подписка отсутствует', status=status.HTTP_400_BAD_REQUEST)



