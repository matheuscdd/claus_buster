from django.urls import path
from .views import MovieView, MovieViewSpecific

urlpatterns = [
    path('movies/', MovieView.as_view()),
    path('movies/<int:movie_id>/', MovieViewSpecific.as_view())
]

