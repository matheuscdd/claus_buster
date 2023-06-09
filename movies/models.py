from django.db import models
from users.models import User


class Rating(models.TextChoices):
    G = 'G'
    R = 'R'
    PG = 'PG'
    PG_13 = 'PG-13'
    NC_17 = 'NC-17'


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, null=True, default=None)
    synopsis = models.TextField(null=True, default=None)
    rating = models.CharField(max_length=20, null=True, default=Rating.G, choices=Rating.choices)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='movies')
    user_many = models.ManyToManyField(
        User,
        through='MovieOrder',
        related_name='movie_many'
    )

    def __repr__(self):
        return f'<Movie [{self.pk}] {self.title} - {self.user.username}>'


class MovieOrder(models.Model):
    buyed_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __repr__(self):
        return f'<MovieOrder [{self.pk}] {self.users.username} - {self.movies.title} (R${self.price})>'
