from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Movie, Actor

class MovieModelTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

        self.actor1 = Actor.objects.create(name='Actor 1')
        self.actor2 = Actor.objects.create(name='Actor 2')

        self.movie1 = Movie.objects.create(title="Movie 1", duration=120, rating=5)
        self.movie1.actors.add(self.actor1, self.actor2)
        self.movie1.favorited_by.add(self.user1)

        self.movie2 = Movie.objects.create(title="Movie 2", duration=100, rating=4)
        self.movie2.actors.add(self.actor1)
        self.movie2.favorited_by.add(self.user1, self.user2)

    def test_valid(self):
        movie = Movie(title="Test Movie", duration=120, rating=5)
        self.assertTrue(movie.is_valid())
    
    def test_invalid_duration(self):
        movie = Movie(title="Test Movie", duration=-5, rating=5)
        self.assertFalse(movie.is_valid())

    def test_invalid_rating(self):
        movie = Movie(title="Test Movie", duration=120, rating=6)
        self.assertFalse(movie.is_valid())
        
    def test_invalid_duration_and_rating(self):
        movie = Movie(title="Test Movie", duration=-5, rating=0)
        self.assertFalse(movie.is_valid())
        
    def test_favorites(self):
        # Test that users have correct favorite movies
        self.assertEqual(list(self.user1.favorite_movies.all()), [self.movie1, self.movie2])
        self.assertEqual(list(self.user2.favorite_movies.all()), [self.movie2])

    def test_actors(self):
        # Test that movies have correct actors
        self.assertEqual(list(self.movie1.actors.all()), [self.actor1, self.actor2])
        self.assertEqual(list(self.movie2.actors.all()), [self.actor1])


class MovieViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.movie1 = Movie.objects.create(title="Movie 1", duration=120, rating=5)
        self.movie2 = Movie.objects.create(title="Movie 2", duration=100, rating=4)
        
    def test_index_view(self):
        # Use the client to perform actions just like a user
        response = self.client.get(reverse('index'))

        # Check that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the correct templates were used
        self.assertTemplateUsed(response, 'movies/index.html')

        # Check that the context data contains the right movies
        movies_in_context = response.context['movies']
        self.assertEqual(list(movies_in_context), [self.movie1, self.movie2])

        # Check that the movie titles appear in the rendered HTML
        self.assertContains(response, str(self.movie1.title))
        self.assertContains(response, str(self.movie2.title))
