from rest_framework.views import APIView, Request, Response, status
from users.permissions import IsEmployeeOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import MovieSerializer
from .serializers import MovieOrderSerializer
from django.shortcuts import get_object_or_404
from .models import Movie
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrReadOnly]

    def post(self, req: Request) -> Response:
        serializer = MovieSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=req.user)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, req: Request) -> Response:
        movies = Movie.objects.all()
        result_page = self.paginate_queryset(movies, req, view=self)
        serializer = MovieSerializer(instance=result_page, many=True)
        return self.get_paginated_response(serializer.data)


class MovieViewSpecific(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrReadOnly]

    def delete(self, req: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, pk=movie_id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, req: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, pk=movie_id)
        serializer = MovieSerializer(instance=movie)
        return Response(serializer.data, status.HTTP_200_OK)

class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, req: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, pk=movie_id)
        # req.data['users'] = req.user
        # req.data['movies'] = movie
        # set_trace()
        serializer = MovieOrderSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(users=req.user, movies=movie)
        return Response(serializer.data, status.HTTP_201_CREATED)
