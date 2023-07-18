from rest_framework.authtoken.models import Token
import pandas as pd
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import (WatchListSerializer, StreamPlatformSerializer, 
                                            ReviewSerializer)
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from watchlist_app.api.permission import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle

class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)
    
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)


@api_view(['POST'])
def stream_platform_bulkcreate(request):
    uploaded_file = request.FILES.get("uploaded_file")
    df = pd.read_csv(uploaded_file)
    platforms = []
    for index, row in df.iterrows():
        platforms.append(
            StreamPlatform(
                name=row["name"],
                about=row["about"],
                website=row["website"],
            )
        )
    StreamPlatform.objects.bulk_create(platforms)
    return Response({"message": "Succesfully bulk created the platforms!"})

@api_view(['POST'])
def watchlist_bulkcreate(request):
    uploaded_file = request.FILES.get("uploaded_file")
    df = pd.read_csv(uploaded_file)
    watchlist = []
    for index, row in df.iterrows():
        instance = StreamPlatform.objects.get(id=row['platform'])
        active = bool(row['active'])
        watchlist.append(
            WatchList(
                title=row["title"],
                storyline=row["storyline"],
                platform=instance,
                active=active,
            )
        )
    WatchList.objects.bulk_create(watchlist)
    return Response({"message": "Successfully bulk created the watchlist!"})

@api_view(['POST'])
def review_bulkcreate(request):
    uploaded_file = request.FILES.get("uploaded_file")
    df = pd.read_csv(uploaded_file)
    review = []
    for index, row in df.iterrows():
        watchlist = WatchList.objects.get(id=row['watchlist'])
        review_user = User.objects.get(id=row['user'])
        active = bool(row['active'])
        review.append(
            Review(
                rating=row["rating"],
                description=row["description"],
                watchlist=watchlist,
                review_user=review_user,
                active=active,
            )
        )
    Review.objects.bulk_create(review)

    movie_ratings = {}
    for review_obj in review:
        movie = review_obj.watchlist
        rating = review_obj.rating
        if movie.id in movie_ratings:
            # Accumulate the total rating and increment the count
            movie_ratings[movie.id]["total_rating"] += rating
            movie_ratings[movie.id]["count"] += 1
            movie_ratings[movie.id]["number_rating"] += 1
        else:
            # Initialize the movie's rating information
            movie_ratings[movie.id] = {
                "total_rating": rating,
                "count": 1,
                "number_rating": 1,
            }

    # Update average ratings for movies
    for movie_id, rating_info in movie_ratings.items():
        movie = WatchList.objects.get(id=movie_id)
        total_rating = rating_info["total_rating"]
        count = rating_info["count"]
        number_rating = rating_info["number_rating"]
        movie.avg_rating = total_rating / count
        movie.number_rating = number_rating
        movie.save()


    return Response({"message": "Successfully bulk created the review!"})


@api_view(['POST'])
def user_bulkcreate(request):
    uploaded_file = request.FILES.get("uploaded_file")
    df = pd.read_csv(uploaded_file)
    users = []
    for index, row in df.iterrows():
        user = User(
            username=row["username"],
            password=make_password(row["password"]),
            email=row["email"],
        )
        users.append(user)
    User.objects.bulk_create(users)
    
    for user in users:
        # Generate token for each user
        token = Token.objects.create(user=user)
        user.token = token.key
        user.save()
    return Response({"message": "Successfully bulk created the user!"})

class ReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        
        user = self.request.user
        review_queryset = Review.objects.filter(watchlist=movie, review_user=user)
        
        if review_queryset.exists():
            raise ValidationError("Already reviewed this movie.")
        
        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating =(movie.avg_rating+serializer.validated_data['rating'])/2
            
        movie.number_rating = movie.number_rating + 1
        movie.save()
        
        serializer.save(watchlist=movie, review_user=user)

class ReviewList(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    

# class ReviewList(mixins.ListModelMixin,
#                 mixins.CreateModelMixin,
#                 generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class= ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]

# class StreamPlatformVS(viewsets.ViewSet):
#     """
#     A simple ViewSet for listing or retrieving users.
#     """
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchList = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(StreamPlatform)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

class StreamPlatformListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        platfrom = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platfrom, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self,request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)  # Retrieve a specific movie object based on the provided primary key (pk)
        except WatchList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamPlatformSerializer(platform)  # Serialize the movie object
        return Response(serializer.data)  # Return the serialized data as a JSON response
    
    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)  # Retrieve a specific movie object based on the provided primary key (pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)  # Retrieve a specific movie object based on the provided primary key (pk)
        platform.delete()  # Delete the movie object from the database
        return Response(status=status.HTTP_204_NO_CONTENT)

class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)  # Retrieve a specific movie object based on the provided primary key (pk)
        except WatchList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie)  # Serialize the movie object
        return Response(serializer.data)  # Return the serialized data as a JSON response
    
    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)  # Retrieve a specific movie object based on the provided primary key (pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)  # Retrieve a specific movie object based on the provided primary key (pk)
        movie.delete()  # Delete the movie object from the database
        return Response(status=status.HTTP_204_NO_CONTENT)

# Import required modules and classes

# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()  # Retrieve all movie objects from the database
#         serializer = MovieSerializer(movies, many=True)  # Serialize the movie objects
#         return Response(serializer.data)  # Return the serialized data as a JSON response
    
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)  # Retrieve a specific movie object based on the provided primary key (pk)
#         except Movie.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         serializer = MovieSerializer(movie)  # Serialize the movie object
#         return Response(serializer.data)  # Return the serialized data as a JSON response

#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)  # Retrieve a specific movie object based on the provided primary key (pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)  # Retrieve a specific movie object based on the provided primary key (pk)
#         movie.delete()  # Delete the movie object from the database
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

# # Define a view function to retrieve details of a specific movie based on the provided primary key (pk)
