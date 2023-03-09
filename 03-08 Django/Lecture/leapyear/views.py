from django.shortcuts import render
import datetime

# Create your views here.
def index(request):
    return render(request, 'leapyear/index.html', {
        'isleapyear': (datetime.datetime.now().year % 4) == 0
    })
