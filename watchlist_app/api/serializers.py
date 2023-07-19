from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ('watchlist',)
        # fields = "__all__"

class WatchListSerializer(serializers.ModelSerializer):
    # review = ReviewSerializer(
    #     many=True,
    #     read_only=True
    #     )
    platform = serializers.CharField(source='platform.name')
    class Meta:
        model = WatchList
        fields = "__all__"
        # fields = ['id', 'name', 'description']
        # exclude =['name']
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='movie_details'
    # )
    class Meta:
        model = StreamPlatform
        fields = "__all__"
        


# def name_length(value):
#         if len(value)<2:
#             raise serializers.ValidationError("Name is too short!")

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validator = [name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
