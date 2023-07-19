from django.contrib import admin
from watchlist_app.models import WatchList, StreamPlatform, Review

# Register your models here.

# admin.site.register(WatchList)
# admin.site.register(StreamPlatform)
# admin.site.register(Review)

@admin.register(WatchList)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['title','platform_name', 'id']
    def platform_name(self,obj):
        return obj.platform.name
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['watchlist', 'rating', 'id', 'get_review_user_username','get_watchlist_id']

    def get_review_user_username(self, obj):
        return obj.review_user.username

    get_review_user_username.short_description = 'Review User'
    
    def get_watchlist_id(self, obj):
        return obj.watchlist.id

    get_watchlist_id.short_description = 'watchlist_id'
    
@admin.register(StreamPlatform)
class StreamPlatformAdmin(admin.ModelAdmin):
    list_display = ['name','website', 'id']