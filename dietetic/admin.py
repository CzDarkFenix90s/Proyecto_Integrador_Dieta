from django.contrib import admin
from dietetic.models import PlanNutricional, AlimentoProgramado, ConsultaDietetica, SeguimientoNutricional
from dietetic.models.categoria_alimento import CategoriaAlimento
from dietetic.models.detalle_plan_alimento import DetallePlanAlimento
from dietetic.models.factura_pagos import FacturaPago
from dietetic.models.momento_comida import MomentoComida
from dietetic.models.nutricionista import Nutricionista
from dietetic.models.paciente import Paciente
from dietetic.models.diaplan import DiaPlan
from dietetic.models.registro_ejercicio import RegistroEjercicio
from dietetic.models.rutina_ejercicio import RutinaEjercicio


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


@admin.register(Nutricionista)
class NutricionistaAdmin(admin.ModelAdmin):
    list_display  = ['id', 'user', 'specialty', 'is_active', 'created_at']
    list_filter   = ['is_active', 'specialty']
    search_fields = ['user__first_name', 'user__last_name', 'specialty']

@admin.register(CategoriaAlimento)
class CategoriaAlimentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'descripcion', 'estado', 'created_at']
    list_filter = ['estado', 'created_at']
    search_fields = ['nombre', 'descripcion']

@admin.register(DiaPlan)
class DiaPlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'plan_nutricional', 'dia_semana', 'descripcion', 'created_at']
    list_filter = ['plan_nutricional', 'dia_semana']
    search_fields = ['descripcion']
    search_fields = ['patient_code', 'full_name', 'user__first_name', 'user__last_name']

@admin.register(MomentoComida)
class MomentoComidaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'descripcion', 'created_at']
    list_filter = ['created_at']
    search_fields = ['nombre', 'descripcion']

@admin.register(DetallePlanAlimento)
class DetallePlanAlimentoAdmin(admin.ModelAdmin):
    list_display  = ['id', 'plan_nutricional', 'alimento_programado', 'quantity', 'observations', 'is_active', 'created_at']
    list_filter   = ['is_active', 'plan_nutricional', 'alimento_programado']
    search_fields = ['plan_nutricional__name', 'alimento_programado__name', 'observations']

@admin.register(FacturaPago)
class FacturaPagoAdmin(admin.ModelAdmin):
    list_display  = ['id', 'invoice_number', 'paciente', 'consulta', 'payment_method', 'total_amount', 'status', 'payment_date', 'created_at']
    list_filter   = ['status', 'payment_method', 'payment_date']
    search_fields = ['invoice_number', 'paciente__full_name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(RegistroEjercicio)
class RegistroEjercicioAdmin(admin.ModelAdmin):
    list_display  = ['id', 'paciente', 'rutina_ejercicio', 'fecha', 'completado', 'created_at']
    list_filter   = ['completado', 'fecha', 'rutina_ejercicio']
    search_fields = ['paciente__patient_code', 'paciente__full_name', 'rutina_ejercicio__descripcion_rutina']

@admin.register(RutinaEjercicio)
class RutinaEjercicioAdmin(admin.ModelAdmin):
    list_display  = ['id', 'plan_nutricional', 'descripcion_rutina', 'dias_semana', 'duracion_minutos', 'created_at']
    list_filter   = ['plan_nutricional', 'dias_semana']
    search_fields = ['plan_nutricional__name', 'descripcion_rutina', 'dias_semana']