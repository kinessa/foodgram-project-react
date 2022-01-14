from rest_framework import status
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.pagination import CustomPageNumberPagination
from .models import Follow, CustomUser
from .serializers import UserSerializer, ShowFollowersSerializer, FollowSerializer


class FollowView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, user_id):
        user = request.user
        author = get_object_or_404(CustomUser, id=user_id)
        if Follow.objects.filter(user=user, id=user_id).exists():
            return Response('Уже подписаны', status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.create(user=user, author=author)
        serializer = FollowSerializer
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        user = request.user
        following = get_object_or_404(CustomUser, id=user_id)
        follow = get_object_or_404(Follow, user=user, author=following)
        if not follow:
            return Response('Не подписаны', status=status.HTTP_400_BAD_REQUEST)
        follow.delete()
        return Response('Удалено', status=status.HTTP_204_NO_CONTENT)


class FollowListView(ListAPIView):
    pagination_class = CustomPageNumberPagination
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        queryset = CustomUser.objects.filter(following=user)
        page = self.paginate_queryset(queryset)
        serializer = ShowFollowersSerializer(
            page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
