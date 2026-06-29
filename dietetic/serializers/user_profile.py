from rest_framework import serializers
from django.core.exceptions import ValidationError
from dietetic.models.user_profile import UserProfile


def validate_image(image):
    max_size = 2 * 1024 * 1024  
    if image.size > max_size:
        raise ValidationError("El tamaño máximo de la imagen es 2MB")
    
    valid_formats = ['image/jpeg', 'image/png', 'image/webp']
    if image.content_type not in valid_formats:
        raise ValidationError("Solo se permiten imágenes en formato JPG, PNG o WebP")
    
    return image


class UserProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    user_id = serializers.PrimaryKeyRelatedField(source='user', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user_id', 'username', 'email', 'role', 'avatar', 'avatar_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
        return None

    def update(self, instance, validated_data):
        avatar = validated_data.get('avatar')
        if avatar:
            validate_image(avatar)
        return super().update(instance, validated_data)