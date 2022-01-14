from django.urls import include, path
from .view import FollowView

urlpatterns = [
    path('users/<int:id>/subscribe/', FollowView.as_view(), name='subscribe'),
    path('users/subscriptions/', FollowView.as_view(), name='subscription'),
    # path('users/subscriptions/', show_follower, name='users_subs'),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
