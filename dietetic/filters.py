# dietetic/filters.py
import django_filters
from dietetic.models import PlanNutricional, AlimentoProgramado, ConsultaDietetica


class PlanNutricionalFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model  = PlanNutricional
        fields = ['is_active']


class AlimentoProgramadoFilter(django_filters.FilterSet):
    name             = django_filters.CharFilter(lookup_expr='icontains')
    portion_min      = django_filters.NumberFilter(field_name='portion_grams', lookup_expr='gte')
    portion_max      = django_filters.NumberFilter(field_name='portion_grams', lookup_expr='lte')
    sequence_min     = django_filters.NumberFilter(field_name='sequence', lookup_expr='gte')
    sequence_max     = django_filters.NumberFilter(field_name='sequence', lookup_expr='lte')
    plan_name        = django_filters.CharFilter(
        field_name='plan_nutricional__name', lookup_expr='icontains'
    )

    class Meta:
        model  = AlimentoProgramado
        fields = ['is_active', 'meal_type', 'plan_nutricional']


class ConsultaDieteticaFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name='scheduled_time', lookup_expr='date__gte')
    to_date   = django_filters.DateFilter(field_name='scheduled_time', lookup_expr='date__lte')

    class Meta:
        model  = ConsultaDietetica
        fields = ['status', 'plan_nutricional', 'paciente', 'nutricionista']
