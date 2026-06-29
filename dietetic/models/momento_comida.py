# dietetic/models/momento_comida.py
from django.db import models


class MomentoComida(models.Model):
    MOMENTOS = [
        ("DESAYUNO", "Desayuno"),
        ("MEDIA_MANANA", "Media Mañana"),
        ("ALMUERZO", "Almuerzo"),
        ("MERIENDA", "Merienda"),
        ("CENA", "Cena"),
        ("SNACK", "Snack"),
    ]

    nombre = models.CharField(
        max_length=20,
        choices=MOMENTOS,
        unique=True
    )

    descripcion = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "momento_comida"
        verbose_name = "Momento de comida"
        verbose_name_plural = "Momentos de comida"
        ordering = ["id"]

    def __str__(self):
        return self.get_nombre_display()