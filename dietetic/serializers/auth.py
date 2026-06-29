from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.db.models import Q

User = get_user_model()

class CustomTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email']    = user.email
        token['is_staff'] = user.is_staff

        # Determinar rol
        if user.is_superuser:
            token['role'] = 'admin'
        elif hasattr(user, 'nutricionista_profile'):
            token['role'] = 'nutricionista'
        else:
            token['role'] = 'paciente'

        return token

    def validate(self, attrs):
        # Permitir login con username o email
        username_or_email = attrs.get("username")

        # Buscar el usuario por username o email
        user = User.objects.filter(
            Q(username__iexact=username_or_email) | Q(email__iexact=username_or_email)
        ).first()

        if user:
            attrs["username"] = user.username

        data = super().validate(attrs)

        data['user_id']  = self.user.id
        data['username'] = self.user.username
        data['email']    = self.user.email
        data['is_staff'] = self.user.is_staff

        # Determinar rol para el frontend
        if self.user.is_superuser:
            data['role'] = 'admin'
        elif hasattr(self.user, 'nutricionista_profile'):
            data['role'] = 'nutricionista'
        else:
            data['role'] = 'paciente'

        return data


class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


# === SERIALIZERS FALTANTES PARA EL RESTABLECIMIENTO DE CONTRASEÑA ===

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("No existe ningún usuario registrado con este correo electrónico.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})

    def validate(self, attrs):
        try:
            # Decodificar el ID del usuario
            uid = force_str(urlsafe_base64_decode(attrs['uidb64']))
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({'uidb64': 'El enlace de restablecimiento no es válido o ha expirado.'})

        # Verificar el token único de seguridad de Django
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise serializers.ValidationError({'token': 'El token de seguridad es inválido o ya fue utilizado.'})

        return attrs

    def save(self):
        # Cambiar la contraseña de forma segura utilizando hashing
        self.user.set_password(self.validated_data['password'])
        self.user.save()
        return self.user