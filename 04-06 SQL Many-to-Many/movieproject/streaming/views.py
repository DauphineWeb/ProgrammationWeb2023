from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import Http404
from streaming.models import Movie

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    return render(request, 'streaming/index.html', {'movies': movies})

def movie(request, movie_id):
    try:
        print(Movie.objects.get(pk=movie_id))
        movie = Movie.objects.get(pk=movie_id)
        return render(request, 'streaming/movie.html', {'movie': movie})
    except ObjectDoesNotExist:
        raise Http404('Movie not found')
