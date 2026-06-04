from django.db import models
from django.contrib.auth.models import User


class Nutricionista(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='nutricionista_profile',
        null=True,
        blank=True
    )
    first_name          = models.CharField(max_length=100)
    last_name           = models.CharField(max_length=100)
    professional_id     = models.CharField(max_length=50, unique=True)
    specialty           = models.CharField(max_length=120)
    consultation_fee    = models.DecimalField(max_digits=10, decimal_places=2)
    consultations_completed = models.PositiveIntegerField(default=0)
    is_active           = models.BooleanField(default=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def fee_with_bonus(self):
        return round(float(self.consultation_fee) * 1.15, 2)

    @property
    def is_experienced(self):
        return self.consultations_completed > 0
