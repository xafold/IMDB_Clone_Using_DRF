from watchlist_app.models import WatchList, StreamPlatform
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class StreamPlatformListAV(APIView):
    
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
# # Define a view function to list movies


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
