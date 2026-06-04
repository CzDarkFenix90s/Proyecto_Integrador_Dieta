# dietetic/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from dietetic.views.health      import health_check
from dietetic.views.auth        import RegisterView, LogoutView
from dietetic.views.user                import UserViewSet
from dietetic.views.plan_nutricional    import PlanNutricionalViewSet
from dietetic.views.alimento_programado import AlimentoProgramadoViewSet
from dietetic.views.consulta_dietetica  import ConsultaDieteticaViewSet
from dietetic.views.paciente            import PacienteViewSet
from dietetic.views.nutricionista       import NutricionistaViewSet
from dietetic.serializers.auth          import CustomTokenView

router = DefaultRouter()
router.register('users',           UserViewSet,                 basename='user')
router.register('pacientes',       PacienteViewSet,             basename='paciente')
router.register('nutricionistas',  NutricionistaViewSet,        basename='nutricionista')
router.register('planes',          PlanNutricionalViewSet,      basename='plan-nutricional')
router.register('alimentos',       AlimentoProgramadoViewSet,   basename='alimento')
router.register('consultas',       ConsultaDieteticaViewSet,    basename='consulta')

urlpatterns = [
    path('health/',             health_check),
    path('auth/register/',      RegisterView.as_view(), name='register'),
    path('auth/login/',         CustomTokenView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('auth/token/verify/',  TokenVerifyView.as_view()),
    path('auth/logout/',        LogoutView.as_view()),
    path('', include(router.urls)),
]
