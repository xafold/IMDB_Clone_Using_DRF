
from django.urls import path
# from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api.views import WatchListAV, WatchDetailAV, StreamPlatformListAV, StreamPlatformDetailAV


urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie_list'),
    path('<int:pk>', WatchDetailAV.as_view(), name='movie_details' ),
    path('stream/', StreamPlatformListAV.as_view(), name ='streamplatform_list'),
    path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name ='streamplatform_details')
]