from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth import views as views_auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.views import View
from django.db.models import Q, Count
from django.views.generic import TemplateView,  UpdateView, DeleteView

from americana.models import Constancia, Tesis, Publicacion, Area, Autor


class Home(TemplateView):
    template_name = 'americana/index.html'


class Tablero(LoginRequiredMixin, View):
    template_name = 'americana/dashboard.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        paginate_by = request.GET.get('paginate_by', self.paginate_by)

        tesis_list = Tesis.objects.all()
        publicacion_list = Publicacion.objects.all()

        tesis_paginator = Paginator(tesis_list, paginate_by)
        publicacion_paginator = Paginator(publicacion_list, paginate_by)

        if request.htmx:
            model_name = request.GET.get('model')
            page_number = request.GET.get('page', 1)
            if model_name == 'tesis':
                tesis_obj = tesis_paginator.get_page(page_number)
                self.template_name = 'americana/tesis/partials/table-dashboard.html'
                context = {'tesis': tesis_obj}
            elif model_name == 'publicacion':
                publicacion_obj = publicacion_paginator.get_page(page_number)
                self.template_name = 'americana/publicacion/partials/table-dashboard.html'
                context = {'publicaciones': publicacion_obj}
        else:
            tesis_obj = tesis_paginator.get_page(1)
            publicacion_obj = publicacion_paginator.get_page(1)
            context = {
                'tesis': tesis_obj,
                'publicaciones': publicacion_obj,
                'tesis_count': Tesis.objects.all().count(),
                'publicaciones_count': Publicacion.objects.all().count()
            }

        return render(request, self.template_name, context)


class LoginView(views_auth.LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_superuser:
            return '/admin'
        else:
            return '/tablero'


class TesisListView(View):
    model = Tesis
    template_name = 'americana/tesis/list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if request.htmx:
            self.template_name = 'americana/tesis/partials/table.html'
            q = request.GET.get('q', '')
            tesis_list = self.model.objects.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )
        else:
            tesis_list = self.model.objects.all()

        paginate_by = request.GET.get('paginate_by', self.paginate_by)
        paginator = Paginator(tesis_list, paginate_by)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context = {
            'tesis': page_obj
        }
        return render(request, self.template_name, context)


class TesisUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tesis
    template_name = "americana/tesis/form.html"
    fields = (
        'file', 'title', 'autor', 'program', 'director', 'co_director', 'description'
    )
    success_url = reverse_lazy('repo-ame:tablero')
    success_message = "%(title)s se ha actualizado correctamente."


class TesisDeleteView(LoginRequiredMixin, DeleteView):
    model = Tesis
    template_name = 'americana/tesis/delete.html'
    success_url = reverse_lazy('repo-ame:tablero')


class PublicacionListView(View):
    model = Publicacion
    template_name = 'americana/publicacion/list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if request.htmx:
            self.template_name = 'americana/publicacion/partials/table.html'
            q = request.GET.get('q', '')
            publicaciones_list = self.model.objects.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )
        else:
            publicaciones_list = self.model.objects.all()

        paginate_by = request.GET.get('paginate_by', self.paginate_by)
        paginator = Paginator(publicaciones_list, paginate_by)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context = {
            'publicaciones': page_obj
        }
        return render(request, self.template_name, context)


class PublicacionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Publicacion
    template_name = 'americana/publicacion/form.html'
    fields = (
        'file', 'title', 'autor', 'conference', 'description',
        'isbn', 'issn', 'publish_date'
    )
    success_url = reverse_lazy('repo-ame:tablero')
    success_message = "%(title)s se ha actualizado correctamente."


class PublicacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Publicacion
    template_name = 'americana/publicacion/delete.html'
    success_url = reverse_lazy('repo-ame:tablero')


@require_http_methods(['GET'])
def publicacion_modal_summary(request, pk):
    template_name = 'americana/publicacion/partials/modal.html'
    context = {
        'publicacion': Publicacion.objects.get(pk=pk)
    }
    return render(
        request, template_name, context
    )


@require_http_methods(['GET'])
def tesis_modal_summary(request, pk):
    template_name = 'americana/tesis/partials/modal.html'
    context = {
        'tesis': Tesis.objects.get(pk=pk)
    }
    return render(
        request, template_name, context
    )


def index(request):
    context = {}
    context['publicaciones'] = Publicacion.objects.all()[:10]
    context['areas'] = Area.objects.all()
    context['anios'] = Publicacion.objects.values('publish_date')\
        .annotate(count=Count('id')).values('publish_date', 'count').order_by('-count')[:3]
    context['autores'] = Autor.objects.all().exclude(id=1)
    return render(request, 'index.html', context)


def search(request):
    print(request.GET)
    context = {}
    tipo = request.GET.get('tipo', 'publicaciones')
    paginate_by = request.GET.get('paginate_by', 10)
    params = {key: data for key, data in request.GET.items()}
    models = {
        'tesis': Tesis,
        'constancias': Constancia,
        'publicaciones': Publicacion
    }

    if tipo == 'tesis' and params.get('programa', ''):
        qs = Tesis.objects.filter(
            program=params.get('programa')
        )
    else:
        qs = models[tipo].objects.filter(
            Q(autor__slug=params.get('autor', '')) |
            Q(area__slug=params.get('area', '')) |
            Q(publish_date__year=params.get('anio', 1970))
        )

    if request.GET.get('q', ''):
        q = request.GET.get('q', '')
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

    paginator = Paginator(qs, paginate_by)
    page_number = request.GET.get('page', 1)

    if request.htmx:
        template_name = 'partials/list-items.html'
    else:
        template_name = 'filter.html'

    context['obj_list'] = paginator.get_page(page_number)
    b_key = list(params.keys())[0]
    context['breadcrumb_key'] = 'Año' if 'anio' in b_key else b_key
    context['breadcrumb_value'] = ' '.join(list(params.values())[0].split('-'))
    return render(request, template_name, context)
