from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'users/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        return render(request, 'users/login.html', {
            'error': 'Username or password were wrong.'
        })
    else:
        return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')