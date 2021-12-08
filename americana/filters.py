import django_filters
from django.db.models import Q, query

from americana.models import Tesis, Congreso

class TesisFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search')
    class Meta:
        model = Tesis
        fields = ['q', ]
    
    def search(self, queryset, name, value):
        return queryset.filter(
            Q(autor__first_name__icontains=value) | Q(autor__last_name__icontains=value)| \
                Q(title__icontains=value) | Q(program__icontains=value) | \
                    Q(director__icontains=value) | Q(co_director__icontains=value)
        )
    

class CongresoFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search')
    class Meta:
        model = Congreso
        fields = ['q', ]
    
    def search(self, queryset, name, value):
        return queryset.filter(
            Q(student__first_name__icontains=value) | Q(student__last_name__icontains=value)| \
                Q(generation__icontains=value) |  Q(conference__icontains=value) | Q(article__icontains=value)
        )
