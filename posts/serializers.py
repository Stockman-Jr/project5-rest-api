from rest_framework import serializers
from django.core.files.images import get_image_dimensions
from .models import BasePost, Post, PokemonBuild, EV_CHOICE_STATS, GAME_CHOICES
from pokemons.models import Pokemon
from likes.models import Like


class BasePostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    post_category = serializers.SerializerMethodField()

    class Meta:
        model = BasePost
        fields = ['id', 'owner', 'content',
                  'created_at', 'updated_at',
                  'post_type', 'game_filter',
                  'post_category'
                  ]

    def get_post_category(self, obj):
        if isinstance(obj, Post):
            return 'post'
        elif isinstance(obj, PokemonBuild):
            return 'pokemon_build'
        else:
            return ''


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.trainerprofile.id')
    profile_image = serializers.ReadOnlyField(
        source='owner.trainerprofile.avatar.url'
        )
    post_type = serializers.CharField(initial="Game Related")
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    game_filter_display = serializers.CharField(
        source='get_game_filter_display',
        read_only=True
        )

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
        return image

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request:
            return request.user == obj.owner
        return False

    def get_like_id(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            like = Like.objects.filter(owner=request.user, post=obj).first()
            return like.id if like else None
        return None

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'profile_id', 'is_owner',
            'profile_image', 'created_at', 'updated_at',
            'title', 'content', 'image', 'game_filter',
            'ingame_name', "post_type", 'likes_count',
            'like_id', 'comments_count', 'game_filter_display',
        ]


class PokeBuildSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    ev_stats = serializers.MultipleChoiceField(choices=EV_CHOICE_STATS)
    profile_id = serializers.ReadOnlyField(source='owner.trainerprofile.id')
    profile_image = serializers.ReadOnlyField(
        source='owner.trainerprofile.avatar.url'
        )
    post_type = serializers.CharField(initial="Pokémon Build")
    like_id = serializers.SerializerMethodField()
    pokemon_id = serializers.ReadOnlyField(source='pokemon.pokemon.id')
    caught_id = serializers.ReadOnlyField(source='pokemon.id')
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    game_filter_display = serializers.CharField(
        source='get_game_filter_display',
        read_only=True
        )

    def get_fields(self, *args, **kwargs):
        fields = super(PokeBuildSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            fields['pokemon'].queryset = fields['pokemon'].queryset.filter(
                owner=request.user
                )
        return fields

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request:
            return request.user == obj.owner
        return False

    def get_like_id(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            like = Like.objects.filter(owner=request.user, post=obj).first()
            return like.id if like else None
        return None

    def to_internal_value(self, data):
        mutable_data = data.copy()
        try:
            mutable_data['held_item'] = HeldItem.objects.get(
                name=mutable_data['held_item']
                ).pk
        except HeldItem.DoesNotExist:
            pass
        try:
            mutable_data['nature'] = Nature.objects.get(
                name=mutable_data['nature']
                ).pk
        except Nature.DoesNotExist:
            pass
        return super().to_internal_value(mutable_data)

    def to_representation(self, instance):
        ret = super(PokeBuildSerializer, self).to_representation(instance)
        ret['pokemon'] = instance.pokemon.pokemon.name
        ret['held_item'] = instance.held_item.name
        ret['nature'] = instance.nature.name
        return ret

    class Meta:
        model = PokemonBuild
        fields = ['id', 'owner', 'is_owner', 'profile_id',
                  'profile_image', 'pokemon', 'created_at', 'updated_at',
                  'move_one', 'move_two', 'move_three', 'move_four',
                  'ability', 'held_item', 'nature', 'ev_stats',
                  'content', 'game_filter', "post_type",
                  'likes_count', 'like_id', 'comments_count',
                  'game_filter_display', 'caught_id', 'pokemon_id']


class AllPostsSerializer(serializers.Serializer):

    def to_representation(self, obj):
        if isinstance(obj, Post):
            serializer = PostSerializer(obj)
        elif isinstance(obj, PokemonBuild):
            serializer = PokeBuildSerializer(obj)
        else:
            serializer = BasePostSerializer(obj)

        data = serializer.data

        if self.context['request'].user.is_authenticated:
            owner = self.context['request'].user
            post = obj
            try:
                like = Like.objects.get(owner=owner, post=post)
                data['like_id'] = like.id
            except Like.DoesNotExist:
                data['like_id'] = None
        else:
            data['like_id'] = None
        return data
