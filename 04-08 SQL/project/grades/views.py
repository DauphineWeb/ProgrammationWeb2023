from django.shortcuts import render, redirect
from .models import ProblemSet, ProblemSetForm

# Create your views here.
def index(request):
    return render(request, 'grades/index.html', {
        'psets': ProblemSet.objects.all()
    })

def add(request):
    if request.method == 'POST':
        form = ProblemSetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    return render(request, 'grades/add.html', {
        'form': ProblemSetForm()
    })

def pset(request, pset_id):
    pset = ProblemSet.objects.get(pk=pset_id)
    return render(request, 'grades/pset.html', {
        'pset': pset,
        'questions': pset.questions.all()
    })
