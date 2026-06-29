from django.db import models
from django.contrib.auth.models import User


class Paciente(models.Model):
    STATUS_CHOICES = [
        ('activo', 'Activo'),
        ('en_seguimiento', 'En seguimiento'),
        ('inactivo', 'Inactivo'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='paciente_profile',
        null=True,
        blank=True
    )
    patient_code           = models.CharField(max_length=20, unique=True)
    first_name             = models.CharField(max_length=100, default='')
    last_name              = models.CharField(max_length=100, default='')
    age                    = models.PositiveIntegerField(default=0)
    goal                   = models.CharField(max_length=200, default='Salud integral')
    dietary_restrictions   = models.TextField(blank=True, default='')
    current_weight         = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    height_cm              = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    status                 = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')
    medical_notes          = models.TextField(blank=True, default='')
    created_at             = models.DateTimeField(auto_now_add=True)
    updated_at             = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def bmi(self):
        height_m = max(float(self.height_cm) / 100, 0.01)
        return round(float(self.current_weight) / (height_m ** 2), 2)

    @property
    def full_name(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'.strip()
        return self.user.username if self.user else 'Sin nombre'

    @property
    def full_profile(self):
        return f'{self.full_name} ({self.patient_code})'

    def __str__(self):
        return f'{self.full_name} — {self.patient_code}'

class SeguimientoNutricional(models.Model):
    paciente    = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='seguimientos',
    )
    weight_kg   = models.DecimalField(max_digits=6, decimal_places=2)
    waist_cm    = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    notes       = models.TextField(blank=True, default='')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def weight_change(self):
        baseline = self.paciente.seguimientos.order_by('created_at').first()
        if baseline is None:
            return 0
        return round(float(self.weight_kg) - float(baseline.weight_kg), 2)

    def __str__(self):
        return f'Seguimiento de {self.paciente.full_name} — {self.weight_kg} kg'
