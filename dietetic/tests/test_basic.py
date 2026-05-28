from django.test import TestCase
from dietetic.models import Paciente, SeguimientoNutricional, Nutricionista, PlanNutricional, AlimentoProgramado, ConsultaDietetica
from django.utils import timezone


class DieteticDomainTest(TestCase):
    def setUp(self):
        self.paciente = Paciente.objects.create(
            patient_code='PAC-001',
            full_name='Ana López',
            age=31,
            goal='Perder 5 kg',
            dietary_restrictions='Sin lácteos',
            current_weight=72.5,
            height_cm=165.0,
            status='activo',
        )
        self.nutricionista = Nutricionista.objects.create(
            first_name='María',
            last_name='García',
            professional_id='NUT-1001',
            specialty='Nutrición clínica',
            consultation_fee=40.00,
            consultations_completed=12,
        )
        self.plan = PlanNutricional.objects.create(
            name='Plan de pérdida',
            description='Alimentación balanceada para pérdida de peso',
            goal='Pérdida de peso',
            target_calories=1800,
            duration_weeks=8,
            estimated_cost=120.00,
        )
        self.alimento = AlimentoProgramado.objects.create(
            name='Avena con berries',
            description='Desayuno alto en fibra',
            portion_grams=120,
            meal_type='desayuno',
            sequence=1,
            plan_nutricional=self.plan,
        )
        self.consulta = ConsultaDietetica.objects.create(
            status='programada',
            session_notes='Primera valoración',
            scheduled_time=timezone.now(),
            estimated_end=timezone.now(),
            plan_nutricional=self.plan,
            paciente=self.paciente,
            nutricionista=self.nutricionista,
        )

    def test_paciente_tracks_nutrition_metrics(self):
        seguimiento = SeguimientoNutricional.objects.create(
            paciente=self.paciente,
            weight_kg=71.2,
            waist_cm=78.5,
            notes='Progreso favorable',
        )

        self.assertEqual(self.paciente.full_profile, 'Ana López (PAC-001)')
        self.assertEqual(self.paciente.bmi, round(72.5 / (1.65 ** 2), 2))
        self.assertEqual(seguimiento.paciente_id, self.paciente.id)

    def test_consulta_links_plan_paciente_y_nutricionista(self):
        self.assertEqual(self.consulta.paciente.full_name, 'Ana López')
        self.assertEqual(self.consulta.nutricionista.full_name, 'María García')
        self.assertEqual(self.consulta.plan_nutricional.name, 'Plan de pérdida')

    def test_alimento_belongs_to_plan(self):
        self.assertEqual(self.alimento.plan_nutricional.goal, 'Pérdida de peso')
        self.assertEqual(self.alimento.estimated_preparation_minutes, round(120 / 30, 2))

