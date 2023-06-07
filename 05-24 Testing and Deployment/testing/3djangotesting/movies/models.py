from django.db import models
from django.contrib.auth.models import User

class Actor(models.Model):
    name = models.CharField(max_length=100)

class Movie(models.Model):
    title = models.CharField(max_length=128)
    duration = models.IntegerField()
    rating = models.SmallIntegerField()
    actors = models.ManyToManyField(Actor)
    favorited_by = models.ManyToManyField(User, related_name='favorite_movies')

    def is_valid(self):
        return (self.duration >= 0) and (1 <= self.rating <= 5)
    
    def __str__(self):
        return f'{self.title} ({self.duration} mins, {self.rating} stars)'
