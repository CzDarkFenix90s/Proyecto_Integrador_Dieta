from django.contrib import admin
from dietetic.models import PlanNutricional, AlimentoProgramado, ConsultaDietetica, DetallePlanAlimento, SeguimientoNutricional
from dietetic.models.categoria_alimento import CategoriaAlimento
from dietetic.models.diaplan import DiaPlan
from dietetic.models.momento_comida import MomentoComida
from dietetic.models.nutricionista import Nutricionista
from dietetic.models.paciente import Paciente
from dietetic.models.perfil_usuario import PerfilUsuario


@admin.register(PlanNutricional)
class PlanNutricionalAdmin(admin.ModelAdmin):
    list_display  = ['id', 'name', 'goal', 'target_calories', 'duration_weeks', 'estimated_cost', 'is_active', 'created_at']
    list_filter   = ['is_active']
    search_fields = ['name', 'goal']


@admin.register(AlimentoProgramado)
class AlimentoProgramadoAdmin(admin.ModelAdmin):
    list_display  = ['id', 'name', 'meal_type', 'portion_grams', 'sequence', 'is_active', 'plan_nutricional']
    list_filter   = ['is_active', 'meal_type', 'plan_nutricional']
    search_fields = ['name', 'description']
    list_editable = ['sequence', 'portion_grams', 'is_active']


@admin.register(ConsultaDietetica)
class ConsultaDieteticaAdmin(admin.ModelAdmin):
    list_display    = ['id', 'plan_nutricional', 'status', 'scheduled_time', 'created_at']
    list_filter     = ['status', 'plan_nutricional']
    search_fields   = ['paciente__first_name', 'paciente__last_name', 'nutricionista__last_name', 'plan_nutricional__name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(DetallePlanAlimento)
class DetallePlanAlimentoAdmin(admin.ModelAdmin):
    list_display  = ['id', 'plan_nutricional', 'alimento_programado', 'quantity', 'observations', 'is_active', 'created_at']
    list_filter   = ['is_active', 'plan_nutricional', 'alimento_programado']
    search_fields = ['plan_nutricional__name', 'alimento_programado__name', 'observations']

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display  = ['id', 'user', 'created_at']
    list_filter   = ['created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']

@admin.register(Nutricionista)
class NutricionistaAdmin(admin.ModelAdmin):
    list_display  = ['id', 'user', 'specialty', 'is_active', 'created_at']
    list_filter   = ['is_active', 'specialty']
    search_fields = ['user__first_name', 'user__last_name', 'specialty']

@admin.register(MomentoComida)
class MomentoComidaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'descripcion', 'created_at']
    list_filter = ['created_at']
    search_fields = ['nombre', 'descripcion']

@admin.register(DiaPlan)
class DiaPlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'plan_nutricional', 'dia_semana', 'descripcion', 'created_at']
    list_filter = ['plan_nutricional', 'dia_semana']
    search_fields = ['descripcion']
    search_fields = ['patient_code', 'full_name', 'user__first_name', 'user__last_name']

@admin.register(CategoriaAlimento)
class CategoriaAlimentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'descripcion', 'estado', 'created_at']
    list_filter = ['estado', 'created_at']
    search_fields = ['nombre', 'descripcion']