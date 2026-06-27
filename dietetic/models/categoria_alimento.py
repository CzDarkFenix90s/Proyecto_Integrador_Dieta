# dietetic/models/categoria_alimento.py

from django.db import models


class CategoriaAlimento(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    estado = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Categoría de Alimento"
        verbose_name_plural = "Categorías de Alimentos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre