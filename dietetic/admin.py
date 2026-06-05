from django.contrib import admin
from dietetic.models import PlanNutricional, AlimentoProgramado, Nutricionista, Paciente, SeguimientoNutricional, ConsultaDietetica


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


@admin.register(Nutricionista)
class NutricionistaAdmin(admin.ModelAdmin):
    list_display  = ['id', 'first_name', 'last_name', 'professional_id', 'specialty', 'consultation_fee', 'is_active']
    list_filter   = ['is_active']
    search_fields = ['first_name', 'last_name', 'professional_id', 'specialty']
    list_editable = ['consultation_fee', 'is_active']


class SeguimientoNutricionalInline(admin.TabularInline):
    model  = SeguimientoNutricional
    extra  = 0
    fields = ['weight_kg', 'waist_cm', 'notes']


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display    = ['id', 'patient_code', 'first_name', 'last_name', 'age', 'goal', 'status', 'current_weight', 'created_at']
    list_filter     = ['status']
    search_fields   = ['patient_code', 'first_name', 'last_name']
    inlines         = [SeguimientoNutricionalInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ConsultaDietetica)
class ConsultaDieteticaAdmin(admin.ModelAdmin):
    list_display    = ['id', 'paciente', 'nutricionista', 'plan_nutricional', 'status', 'scheduled_time', 'created_at']
    list_filter     = ['status', 'plan_nutricional']
    search_fields   = ['paciente__first_name', 'paciente__last_name', 'nutricionista__last_name', 'plan_nutricional__name']
    readonly_fields = ['created_at', 'updated_at']
