from django.db import models
from .consulta_dietetica import ConsultaDietetica
from .paciente import Paciente


class FacturaPago(models.Model):
    PAYMENT_METHODS = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('TRANSFERENCIA', 'Transferencia'),
    ]

    STATUS_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado'),
        ('ANULADO', 'Anulado'),
    ]

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='facturas'
    )

    consulta = models.ForeignKey(
        ConsultaDietetica,
        on_delete=models.CASCADE,
        related_name='facturas'
    )

    invoice_number = models.CharField(
        max_length=30,
        unique=True
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateField()

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PENDIENTE'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-payment_date']
        verbose_name = 'Factura de Pago'
        verbose_name_plural = 'Facturas de Pago'

    def __str__(self):
        return f"{self.invoice_number} - {self.paciente}"