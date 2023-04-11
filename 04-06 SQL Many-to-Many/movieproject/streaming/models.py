from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    def __str__(self) -> str:
        return f'{self.name}: {self.price/100}€'


GENRE_CHOICES = (
    ('Rom', 'Romance'),
    ('Com', 'Comedy'),
    ('Dra', 'Drama'),
    ('Ani', 'Animation'),
    ('Fan', 'Fantasy'),
    ('Act', 'Action')
)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(choices=GENRE_CHOICES, max_length=3)
    subscription_plans = models.ManyToManyField(SubscriptionPlan, related_name='movies')
    def __str__(self) -> str:
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(SubscriptionPlan, null=True, blank=True, on_delete=models.CASCADE, related_name='users')

class Review(models.Model):
    rating = models.SmallIntegerField()
    comment = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')

    def clean(self) -> None:
        super(Review, self).clean()
        if self.rating < 1 or self.rating > 5:
            raise ValidationError({'rating': 'rating must be between 1 and 5'})

    def __str__(self) -> str:
        return f'{self.rating}: {self.comment}'
