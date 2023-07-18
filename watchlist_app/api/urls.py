from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import (
    WatchListAV, WatchDetailAV, ReviewCreate, StreamPlatformVS,UserReview,
    ReviewList, ReviewDetail, stream_platform_bulkcreate, watchlist_bulkcreate,user_bulkcreate,review_bulkcreate
)

router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie_list'),
    path('<int:pk>/', WatchDetailAV.as_view(), name='movie_details'),
    path('', include(router.urls)),
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='create_review'),
    path('<int:pk>/review/', ReviewList.as_view(), name='review_list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review_detail'),
    path('stream_platform_bulkcreate/', stream_platform_bulkcreate, name='stream-platform-bulkcreate'),
    path('watchlist_bulkcreate/', watchlist_bulkcreate, name='watchlist_bulkcreate'),
    path('user_bulkcreate/', user_bulkcreate, name='user_bulkcreate'),
    path('review_bulkcreate/', review_bulkcreate, name='review_bulkcreate'),
    path('review/', UserReview.as_view(), name='user-review'),
]

