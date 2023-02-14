from rest_framework import serializers
from django.core.files.images import get_image_dimensions
from .models import BasePost, Post, PokemonBuild, EV_CHOICE_STATS
from likes.models import Like


class AllPostsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = BasePost
        fields = ['id', 'owner',
                  'created_at', 'updated_at',
                  'post_type', 'game_filter'
                  ]


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    post_type = serializers.CharField(initial="Game Related")
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    def validate_image(self, image):
        filesize = image.size
        width, height = get_image_dimensions(image)

        max_size = 2 * 1024 * 1024
        max_width = 3000
        max_height = 3000

        if filesize > max_size:
            raise serializers.ValidationError(
                    'Image size larger than 2MB!'
                )
        if width > max_width:
            raise serializers.ValidationError(
                    'Image width larger than 3000px!'
                )
        if height > max_height:
            raise serializers.ValidationError(
                    'Image height larger than 3000px!'
                )

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'profile_id', 'is_owner',
            'profile_image', 'created_at', 'updated_at',
            'title', 'content', 'image', 'game_filter',
            'ingame_name', "post_type", 'likes_count',
            'like_id', 'comments_count'
        ]


class PokeBuildSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    ev_stats = serializers.MultipleChoiceField(choices=EV_CHOICE_STATS)
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    post_type = serializers.CharField(initial="Pokémon Build")
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    def get_fields(self, *args, **kwargs):
        fields = super(PokeBuildSerializer, self).get_fields(*args, **kwargs)
        view = self.context['view']
        owner = view.request.user
        fields['pokemon'].queryset = fields['pokemon'].queryset.filter(owner=owner)
        return fields

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = PokemonBuild
        fields = ['id', 'owner', 'is_owner', 'profile_id',
                  'profile_image', 'pokemon', 'created_at', 'updated_at',
                  'move_one', 'move_two', 'move_three', 'move_four',
                  'ability', 'held_item', 'nature', 'ev_stats',
                  'content', 'game_filter', "post_type",
                  'likes_count', 'like_id', 'comments_count']
