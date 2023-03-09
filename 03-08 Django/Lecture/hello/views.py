from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('Hello World')

def hello(request, name):
    return HttpResponse(f'Hello {name.capitalize()}')

def bye(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        return HttpResponse(f'Bye {name}')
    return HttpResponse(f'Not a GET request')
