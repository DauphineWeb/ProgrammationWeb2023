from django.shortcuts import render, redirect
from django import forms

class NewToDo(forms.Form):
    newtodo = forms.CharField(label='New todo')
    level = forms.IntegerField(label='Level of urgency', min_value=1, max_value=3)

todos = ['wash clothes', 'respond to mails']

# Create your views here.
def index(request):
    return render(request, 'todo/index.html', {
        'todos': todos
    })

def remove(request):
    todos.pop()
    return redirect('index')

def add(request):
    return render(request, 'todo/add.html', {
        'form': NewToDo()
    })

def addentry(request):
    if request.method == 'POST':
        form = NewToDo(request.POST)
        if form.is_valid():
            newtodo = form.cleaned_data['newtodo']
            level = form.cleaned_data['level']
            todos.append(f'{newtodo} of level {level}')
        else:
            return redirect('add')
    return redirect('index')