from rest_framework import serializers
from .models import Post, PokemonBuildPost, EV_CHOICE_STATS
from django.core.files.images import get_image_dimensions

EV_CHOICE_STATS = [
        ('hp', 'HP'),
        ('attack', 'Attack'),
        ('defense', 'Defense'),
        ('special_attack', 'Special Attack'),
        ('special_defense', 'Special Defense'),
        ('speed', 'Speed'),
    ]


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
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    image = serializers.ImageField(validators=[image_validator])

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def update(self, instance, validated_data):
        validated_data.pop('image', None)
        return super().update(instance, validated_data)

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'profile_id', 'is_owner',
            'profile_image', 'created_at', 'updated_at',
            'title', 'content', 'image', 'game_filter',
            'ingame_name',
        ]


class PostPokeBuildSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    ev_stats = serializers.MultipleChoiceField(choices=EV_CHOICE_STATS)
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    class Meta:
        model = PokemonBuildPost
        fields = ['id', 'owner', 'profile_id', 'profile_image',
                  'pokemon', 'created_at', 'updated_at',
                  'move_one', 'move_two', 'move_three', 'move_four',
                  'ability', 'held_item', 'nature', 'ev_stats',
                  'game_filter']

