from rest_framework import serializers
from .models import Post
from django.core.files.images import get_image_dimensions


def image_validator(image):
    filesize = image.size
    width, height = get_image_dimensions(image)

    max_size = 2 * 1024 * 1024
    max_width = 2000
    max_height = 2000

    if filesize > max_size:
        raise serializers.ValidationError(
                'Image size larger than 2MB!'
            )
    if width > max_width:
        raise serializers.ValidationError(
                'Image width larger than 2000px!'
            )
    if height > max_height:
        raise serializers.ValidationError(
                'Image height larger than 2000px!'
            )


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    image = serializers.ImageField(validators=[image_validator])

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'content', 'image', 'game_filter',
            'ingame_name',
        ]

