# dietetic/views/__init__.py
from .auth import RegisterView, LogoutView
from .health import health_check
from .plan_nutricional import PlanNutricionalViewSet
from .alimento_programado import AlimentoProgramadoViewSet
from .consulta_dietetica import ConsultaDieteticaViewSet
from .paciente import PacienteViewSet, SeguimientoNutricionalViewSet
from .nutricionista import NutricionistaViewSet
from .categoria_alimento import CategoriaAlimentoViewSet
from .diaplan import DiaPlanViewSet
from .user import UserViewSet
from .momento_comida import MomentoComidaViewSet
from .detalle_plan_alimento import DetallePlanAlimentoViewSet
from .factura_pagos import FacturaPagoViewSet
from .registro_ejercicio import RegistroEjercicioViewSet
from .rutina_ejercicio import RutinaEjercicio
