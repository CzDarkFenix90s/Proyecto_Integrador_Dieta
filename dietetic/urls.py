# dietetic/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

# Imports usando rutas relativas limpias para evitar colisiones
from .views.health      import health_check
from .views.auth        import RegisterView, LogoutView, PasswordResetRequestView, PasswordResetConfirmView
from .views.user        import UserViewSet
from .views.plan_nutricional    import PlanNutricionalViewSet
from .views.alimento_programado import AlimentoProgramadoViewSet
from .views.consulta_dietetica  import ConsultaDieteticaViewSet
from .views.paciente            import PacienteViewSet
from .views.nutricionista       import NutricionistaViewSet
from .views.user_profile        import UserProfileViewSet
from .views.horario_nutricionista import HorarioNutricionistaViewSet
from .views.preferencia_alimentaria import PreferenciaAlimentariaViewSet
from .views.objetivo_paciente   import ObjetivoPacienteViewSet
from .views.logro_paciente      import LogroPacienteViewSet
from .serializers.auth          import CustomTokenView
    
router = DefaultRouter()
router.register('users',           UserViewSet,                 basename='user')
router.register('profiles',        UserProfileViewSet,          basename='user-profile')
router.register('pacientes',       PacienteViewSet,             basename='paciente')
router.register('nutricionistas',  NutricionistaViewSet,        basename='nutricionista')
router.register('horarios-nutricionista', HorarioNutricionistaViewSet, basename='horario-nutricionista')
router.register('planes',          PlanNutricionalViewSet,      basename='plan-nutricional')
router.register('alimentos',       AlimentoProgramadoViewSet,   basename='alimento')
router.register('consultas',       ConsultaDieteticaViewSet,    basename='consulta')
router.register('preferencias-alimentarias', PreferenciaAlimentariaViewSet, basename='preferencia-alimentaria')
router.register('objetivos-paciente', ObjetivoPacienteViewSet,  basename='objetivo-paciente')
router.register('logros-paciente', LogroPacienteViewSet,        basename='logro-paciente')


urlpatterns = [
    path('health/',             health_check),
    path('auth/register/',      RegisterView.as_view(), name='register'),
    path('auth/login/',         CustomTokenView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('auth/token/verify/',  TokenVerifyView.as_view()),
    path('auth/logout/',        LogoutView.as_view()),
    
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('auth/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    path('', include(router.urls)),
]