# dietetic/serializers/auth.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.db.models import Q


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
            # Si encontramos al usuario, reemplazamos el campo 'username' con su username real
            # para que el validador base de SimpleJWT pueda autenticarlo correctamente.
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
