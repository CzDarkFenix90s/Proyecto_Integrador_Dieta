from django.db import models
from .plan_nutricional import PlanNutricional
from .alimento_programado import AlimentoProgramado


class DetallePlanAlimento(models.Model):

    plan_nutricional = models.ForeignKey(
        PlanNutricional,
        on_delete=models.PROTECT,
        related_name='detalles_alimentos',
    )

    alimento_programado = models.ForeignKey(
        AlimentoProgramado,
        on_delete=models.PROTECT,
        related_name='detalles_plan',
    )

    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    observations = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.plan_nutricional.name} - {self.alimento_programado.name}'

    @property
    def has_observations(self):
        return bool(self.observations)