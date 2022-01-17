from django.urls import include, path

from .view import FollowView, FollowListView

urlpatterns = [
    path('users/<int:id>/subscribe/', FollowView.as_view(),
         name='subscribe'),
    path('users/subscriptions/', FollowListView.as_view(),
         name='subscription'),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
