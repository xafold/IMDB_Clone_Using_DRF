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
    list_display = ['watchlist','rating', 'id']
    
@admin.register(StreamPlatform)
class StreamPlatformAdmin(admin.ModelAdmin):
    list_display = ['name','website', 'id']