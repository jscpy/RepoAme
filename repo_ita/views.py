from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from repo_ita.models import Articulo
from repo_ita.forms import ArticuloForm


@login_required
def home(request):
    return render(request, 'home.html')


@login_required()
def articulo(request):
    articulos = Articulo.objects.all()
    return render(request, 'articulo/index.html', {'articulos': articulos})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def create_articulo(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.user = request.user
            articulo.save()
            return redirect('home')
    else:
        form = ArticuloForm()
    return render(request, 'articulo.html', {'form': form})
