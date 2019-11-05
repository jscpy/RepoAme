from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from repo_ita.models import Articulo

# Create your views here.
def home(request):
    articulos = Articulo.objects.all()
    return render(request, 'home.html', context={'articulos': articulos})

def signup(request):
    return render(request, 'signup.html')


def register(request):
    # import ipdb; ipdb.set_trace()
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.create_user(username, password)
    if user:
        return redirect('/')
    else:
        return redirect('/register')
