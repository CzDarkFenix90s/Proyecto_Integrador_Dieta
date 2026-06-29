from django.db import models
from .plan_nutricional import PlanNutricional


class DiaPlan(models.Model):
    DIAS = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]

    plan_nutricional = models.ForeignKey(
        PlanNutricional,
        on_delete=models.CASCADE,
        related_name='dias_plan'
    )

    dia_semana = models.CharField(
        max_length=10,
        choices=DIAS
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Día del Plan"
        verbose_name_plural = "Días del Plan"
        ordering = ['id']
        unique_together = ('plan_nutricional', 'dia_semana')

    def __str__(self):
        return f"{self.plan_nutricional} - {self.dia_semana}"