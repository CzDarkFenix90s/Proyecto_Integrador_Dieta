from django.db import models

from dietetic.models.nutricionista import Nutricionista
from dietetic.models.paciente import Paciente
from .plan_nutricional import PlanNutricional


class ConsultaDietetica(models.Model):
    STATUS_CHOICES = [
        ('programada', 'Programada'),
        ('en_curso', 'En curso'),
        ('completada', 'Completada'),
        ('retrasada', 'Retrasada'),
        ('cancelada', 'Cancelada'),
    ]

    status            = models.CharField(max_length=20, choices=STATUS_CHOICES, default='programada')
    session_notes     = models.TextField(blank=True, default='')
    scheduled_time    = models.DateTimeField()
    estimated_end     = models.DateTimeField()
    plan_nutricional  = models.ForeignKey(
        PlanNutricional,
        on_delete=models.CASCADE, # Cambiado a CASCADE para permitir borrado en Admin
        related_name='consultas',
    )
    paciente = models.ForeignKey(
       Paciente,
       on_delete=models.CASCADE,
       related_name='consultas',
       null=True,
       blank=True,
    )

    nutricionista = models.ForeignKey(
       Nutricionista,
       on_delete=models.CASCADE,
       related_name='consultas',
       null=True,
       blank=True,
    )
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_time']

    def __str__(self):
        return f'Consulta #{self.id} — {self.paciente.full_name} ({self.status})'

    @property
    def duration_minutes(self):
        delta = self.estimated_end - self.scheduled_time
        return max(0, round(delta.total_seconds() / 60, 2))

    @property
    def is_delayed(self):
        return self.status == 'retrasada'
