from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import views as views_auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView

from django_filters.views import FilterView

from americana.models import Tesis, Publicacion
from americana.forms import UserForm, ProfileForm
from americana.filters import TesisFilter, PublicacionFilter


class Home(TemplateView):
    template_name = 'americana/index.html'


class Tablero(LoginRequiredMixin, TemplateView):
    template_name = 'americana/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tesis_por_aprobar"] = Tesis.objects.all()
        context["tesis"] = Tesis.objects.all()
        context["publicaciones"] = Publicacion.objects.all()
        return context


class LoginView(views_auth.LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_superuser:
            return '/admin'
        else:
            return '/tablero'


class TesisListView(LoginRequiredMixin, FilterView, ListView):
    model = Tesis
    template_name = 'americana/tesis/list.html'
    context_object_name = 'tesis'
    filterset_class = TesisFilter
    paginate_by = 10


class TesisUserListView(LoginRequiredMixin, ListView):
    model = Tesis
    template_name = "americana/tesis/index.html"
    context_object_name = 'tesis'


class PublicacionListView(LoginRequiredMixin, FilterView, ListView):
    model = Publicacion
    template_name = 'americana/publicacion/list.html'
    context_object_name = 'publicaciones'
    filterset_class = PublicacionFilter
    paginate_by = 10


class PublicacionUserListView(ListView):
    model = Publicacion
    template_name = "americana/publicacion/index.html"
    context_object_name = 'publicaciones'


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/tablero')
    else:
        form = UserCreationForm()
    return render(request, 'americana/signup.html', {'form': form})


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Tú perfil se ha actualizado correctamente.')
            return redirect(reverse_lazy('repo-ame:tablero'))
        else:
            messages.error(request, 'Porfavir corrige los siguientes errores.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'americana/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
