# dietetic/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dietetic.views.detalle_plan_alimento import DetallePlanAlimentoViewSet
from dietetic.views.diaplan import DiaPlanViewSet
from dietetic.views.momento_comida import MomentoComidaViewSet
from dietetic.views.nutricionista import NutricionistaViewSet
from dietetic.views.paciente import PacienteViewSet
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from dietetic.views.health      import health_check
from dietetic.views.auth        import RegisterView, LogoutView
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
router.register('detalles-plan',   DetallePlanAlimentoViewSet,  basename='detalle-plan')
router.register('pacientes',       PacienteViewSet,             basename='paciente')
router.register('nutricionistas',  NutricionistaViewSet,        basename='nutricionista')
router.register('momentos-comida', MomentoComidaViewSet,        basename='momento-comida')
router.register('dias-plan',      DiaPlanViewSet,              basename='dia-plan')

urlpatterns = [
    path('health/',             health_check),
    path('auth/register/',      RegisterView.as_view(), name='register'),
    path('auth/login/',         CustomTokenView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('auth/token/verify/',  TokenVerifyView.as_view()),
    path('auth/logout/',        LogoutView.as_view()),
    path('', include(router.urls)),
]
