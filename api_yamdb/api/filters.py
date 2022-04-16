from django_filters import rest_framework as filters
from reviews.models import Titles


class TitleFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    genre = filters.CharFilter(field_name='genre__slug')
    category = filters.CharFilter(field_name='category__slug')

    class Meta:
        model = Titles
        fields = '__all__'
