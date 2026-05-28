from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dietetic', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Viaje',
        ),
        migrations.DeleteModel(
            name='Parada',
        ),
        migrations.DeleteModel(
            name='MaintenanceRecord',
        ),
        migrations.DeleteModel(
            name='Ruta',
        ),
        migrations.DeleteModel(
            name='Chofer',
        ),
        migrations.DeleteModel(
            name='Bus',
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_code', models.CharField(max_length=20, unique=True)),
                ('full_name', models.CharField(max_length=120)),
                ('age', models.PositiveIntegerField()),
                ('goal', models.CharField(max_length=200)),
                ('dietary_restrictions', models.TextField(blank=True, default='')),
                ('current_weight', models.DecimalField(decimal_places=2, max_digits=6)),
                ('height_cm', models.DecimalField(decimal_places=2, max_digits=6)),
                ('status', models.CharField(choices=[('activo', 'Activo'), ('en_seguimiento', 'En seguimiento'), ('inactivo', 'Inactivo')], default='activo', max_length=20)),
                ('medical_notes', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Nutricionista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('professional_id', models.CharField(max_length=50, unique=True)),
                ('specialty', models.CharField(max_length=120)),
                ('consultation_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('consultations_completed', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='PlanNutricional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, default='')),
                ('goal', models.CharField(max_length=200)),
                ('target_calories', models.PositiveIntegerField()),
                ('duration_weeks', models.PositiveIntegerField()),
                ('estimated_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SeguimientoNutricional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight_kg', models.DecimalField(decimal_places=2, max_digits=6)),
                ('waist_cm', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('notes', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seguimientos', to='dietetic.paciente')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AlimentoProgramado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, default='')),
                ('portion_grams', models.DecimalField(decimal_places=2, max_digits=10)),
                ('meal_type', models.CharField(choices=[('desayuno', 'Desayuno'), ('almuerzo', 'Almuerzo'), ('cena', 'Cena'), ('snack', 'Snack')], default='desayuno', max_length=20)),
                ('sequence', models.PositiveIntegerField(default=1)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('plan_nutricional', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='alimentos', to='dietetic.plannutricional')),
            ],
            options={
                'ordering': ['sequence'],
            },
        ),
        migrations.CreateModel(
            name='ConsultaDietetica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('programada', 'Programada'), ('en_curso', 'En curso'), ('completada', 'Completada'), ('retrasada', 'Retrasada'), ('cancelada', 'Cancelada')], default='programada', max_length=20)),
                ('session_notes', models.TextField(blank=True, default='')),
                ('scheduled_time', models.DateTimeField()),
                ('estimated_end', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nutricionista', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='consultas', to='dietetic.nutricionista')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='consultas', to='dietetic.paciente')),
                ('plan_nutricional', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='consultas', to='dietetic.plannutricional')),
            ],
            options={
                'ordering': ['-scheduled_time'],
            },
        ),
    ]

