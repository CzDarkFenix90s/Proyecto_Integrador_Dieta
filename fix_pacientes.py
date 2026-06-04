import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from dietetic.models import Paciente

print("Iniciando vinculación de pacientes...")
for u in User.objects.all():
    p, created = Paciente.objects.get_or_create(
        user=u,
        defaults={
            'patient_code': f'PAC-{u.id:04d}',
            'full_name': (f"{u.first_name} {u.last_name}").strip() or u.username,
            'age': 20,
            'current_weight': 70.0,
            'height_cm': 170.0
        }
    )
    if created:
        print(f"Creado perfil de paciente para usuario: {u.username}")
    else:
        print(f"El usuario {u.username} ya tenía perfil de paciente.")

print("Vinculación completada.")
