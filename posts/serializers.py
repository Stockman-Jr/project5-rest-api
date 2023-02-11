from rest_framework import serializers
from .models import BasePost, Post, PokemonBuild, EV_CHOICE_STATS


class AllPostsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
 
    class Meta:
        model = BasePost
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    post_type = serializers.CharField(initial="Game Related")

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'profile_id', 'is_owner',
            'profile_image', 'created_at', 'updated_at',
            'title', 'content', 'image', 'game_filter',
            'ingame_name', "post_type"
        ]


class PokeBuildSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    ev_stats = serializers.MultipleChoiceField(choices=EV_CHOICE_STATS)
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    post_type = serializers.CharField(initial="Pokémon Build")

    class Meta:
        model = PokemonBuild
        fields = ['id', 'owner', 'profile_id', 'profile_image',
                  'pokemon', 'created_at', 'updated_at',
                  'move_one', 'move_two', 'move_three', 'move_four',
                  'ability', 'held_item', 'nature', 'ev_stats',
                  'content', 'game_filter', "post_type"]
