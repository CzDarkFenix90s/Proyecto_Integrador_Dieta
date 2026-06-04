# dietetic/serializers/auth.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


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
