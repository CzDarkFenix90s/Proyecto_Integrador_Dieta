# dietetic/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dietetic.views.categoria_alimento import CategoriaAlimentoViewSet
from dietetic.views.detalle_plan_alimento import DetallePlanAlimentoViewSet
from dietetic.views.diaplan import DiaPlanViewSet
from dietetic.views.factura_pagos import FacturaPagoViewSet
from dietetic.views.momento_comida import MomentoComidaViewSet
from dietetic.views.nutricionista import NutricionistaViewSet
from dietetic.views.paciente import PacienteViewSet, SeguimientoNutricionalViewSet
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from dietetic.views.health      import health_check
from dietetic.views.auth        import RegisterView, LogoutView
from dietetic.views.registro_ejercicio import RegistroEjercicioViewSet
from dietetic.views.rutina_ejercicio import RutinaEjercicioViewSet
from dietetic.views.user                import UserViewSet
from dietetic.views.plan_nutricional    import PlanNutricionalViewSet
from dietetic.views.alimento_programado import AlimentoProgramadoViewSet
from dietetic.views.consulta_dietetica  import ConsultaDieteticaViewSet

from dietetic.serializers.auth          import CustomTokenView

router = DefaultRouter()
router.register('users',           UserViewSet,                 basename='user')
router.register('planes',          PlanNutricionalViewSet,      basename='plan-nutricional')
router.register('alimentos',       AlimentoProgramadoViewSet,   basename='alimento')
router.register('consultas',       ConsultaDieteticaViewSet,    basename='consulta')
router.register('pacientes',       PacienteViewSet,             basename='paciente')
router.register('nutricionistas',  NutricionistaViewSet,        basename='nutricionista')
router.register('categorias-alimento', CategoriaAlimentoViewSet, basename='categoria-alimento')
router.register('seguimientos', SeguimientoNutricionalViewSet, basename='seguimiento-nutricional')
router.register('dias-plan',      DiaPlanViewSet,              basename='dia-plan')
router.register('momentos-comida', MomentoComidaViewSet,        basename='momento-comida')
router.register('detalles-plan',   DetallePlanAlimentoViewSet,  basename='detalle-plan')
router.register('facturas',     FacturaPagoViewSet,            basename='factura-pago')
router.register('rutinas-ejercicio', RutinaEjercicioViewSet, basename='rutina-ejercicio')
router.register('registros-ejercicio', RegistroEjercicioViewSet, basename='registro-ejercicio')
urlpatterns = [
    path('health/',             health_check),
    path('auth/register/',      RegisterView.as_view(), name='register'),
    path('auth/login/',         CustomTokenView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('auth/token/verify/',  TokenVerifyView.as_view()),
    path('auth/logout/',        LogoutView.as_view()),
    path('users/perfil/',       UserViewSet.as_view({'get': 'perfil'}), name='user-perfil'),
    path('', include(router.urls)),
]
