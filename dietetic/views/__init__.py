# dietetic/views/__init__.py
from .auth import RegisterView, LogoutView
from .health import health_check
from .plan_nutricional import PlanNutricionalViewSet
from .alimento_programado import AlimentoProgramadoViewSet
from .consulta_dietetica import ConsultaDieteticaViewSet
from .detalle_plan_alimento import DetallePlanAlimentoViewSet
from .paciente import PacienteViewSet, SeguimientoNutricionalViewSet
from .nutricionista import NutricionistaViewSet
from .momento_comida import MomentoComidaViewSet
from .user import UserViewSet