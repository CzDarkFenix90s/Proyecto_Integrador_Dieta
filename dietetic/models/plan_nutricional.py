# dietetic/models/plan_nutricional.py
from django.db import models


class PlanNutricional(models.Model):
    name              = models.CharField(max_length=200)
    description       = models.TextField(blank=True, default='')
    goal              = models.CharField(max_length=200)
    target_calories   = models.PositiveIntegerField()
    duration_weeks    = models.PositiveIntegerField()
    estimated_cost    = models.DecimalField(max_digits=10, decimal_places=2)
    is_active         = models.BooleanField(default=True)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} — {self.goal}'

    @property
    def cost_with_tax(self):
        return round(float(self.estimated_cost) * 1.15, 2)

    @property
    def has_description(self):
        return len(self.description) > 0
