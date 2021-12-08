from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import views as views_auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    TemplateView, ListView, CreateView, UpdateView, DeleteView)

from django_filters.views import FilterView

from americana.models import Tesis, Congreso
from americana.forms import UserForm, ProfileForm
from americana.filters import TesisFilter, CongresoFilter


class Home(TemplateView):
    template_name = 'americana/index.html'


class Tablero(LoginRequiredMixin, TemplateView):
    template_name = 'americana/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tesis_por_aprobar"] = Tesis.objects.filter(
            autor=self.request.user, publish=False
        ).count()
        context["tesis"] = Tesis.objects.filter(
            autor=self.request.user
        )
        context["congresos"] = Congreso.objects.filter(
            student=self.request.user
        )
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
    paginate_by = 2
    
    def get_queryset(self):
        return super().get_queryset().filter(
            publish=True
        )


class TesisUserListView(LoginRequiredMixin, ListView):
    model = Tesis
    template_name = "americana/tesis/index.html"
    context_object_name = 'tesis'
    
    def get_queryset(self):
        return super().get_queryset().filter(
            autor=self.request.user
        )


class TesisCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tesis
    template_name = 'americana/tesis/form.html'
    fields = (
        'file', 'title', 'program', 'director', 'co_director'
    )
    success_url = reverse_lazy('repo-ame:tablero')
    success_message = "%(title)s fue creado correctamente."

    def form_valid(self, form):
        tesis = form.save(commit=False)
        tesis.autor = self.request.user
        return super().form_valid(form)


class TesisUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tesis
    template_name = "americana/tesis/form.html"
    fields = (
        'file', 'title', 'program', 'director', 'co_director'
    )
    success_url = reverse_lazy('repo-ame:tablero')
    success_message = "%(title)s se ha actualizado correctamente."


class TesisDeleteView(LoginRequiredMixin, DeleteView):
    model = Tesis
    template_name = 'americana/tesis/delete.html'
    success_url = reverse_lazy('repo-ame:tablero')


class CongresoListView(LoginRequiredMixin, FilterView, ListView):
    model = Congreso
    template_name = 'americana/congreso/list.html'
    context_object_name = 'congresos'
    filterset_class = CongresoFilter
    paginate_by = 10


class CongresoUserListView(ListView):
    model = Congreso
    template_name = "americana/congreso/index.html"
    context_object_name = 'congresos'
    
    def get_queryset(self):
        return super().get_queryset().filter(
            student=self.request.user
        )


class CongresoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Congreso
    template_name = 'americana/congreso/form.html'
    fields = (
        'file', 'generation', 'conference', 'article', 'description'
    )
    success_url = reverse_lazy('repo-ame:tablero')
    success_message = "%(conference)s fue creado correctamente."
    
    def form_valid(self, form):
        congreso = form.save(commit=False)
        congreso.student = self.request.user
        return super().form_valid(form)


class CongresoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Congreso
    template_name = 'americana/congreso/form.html'
    fields = (
        'file', 'generation', 'conference', 'article', 'description'
    )
    success_url = reverse_lazy('repo-ame:tablero')
    success_message = "%(conference)s se ha actualizado correctamente."


class CongresoDeleteView(LoginRequiredMixin, DeleteView):
    model = Congreso
    template_name = 'americana/congreso/delete.html'
    success_url = reverse_lazy('repo-ame:tablero')


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
