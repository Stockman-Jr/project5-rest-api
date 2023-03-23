from rest_framework import serializers
from .models import Pokemon, CaughtPokemon


class PokemonSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()
    types = serializers.StringRelatedField(many=True, read_only=True)
    sprite = serializers.StringRelatedField(read_only=True)
    abilities = serializers.StringRelatedField(many=True, read_only=True)
    moves = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Pokemon
        fields = '__all__'


class CaughtPokemonDetailSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.trainerprofile.id')
    profile_image = serializers.ReadOnlyField(
        source='owner.trainerprofile.avatar.url'
        )
    pokemon = PokemonSerializer()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = CaughtPokemon
        fields = ['id', 'owner', 'profile_id', 'is_owner',
                  'profile_image', 'pokemon']
        depth = 1


class CaughtPokemonSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.trainerprofile.id')
    profile_image = serializers.ReadOnlyField(
        source='owner.trainerprofile.avatar.url'
        )
    pokemon_name = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_pokemon_name(self, obj):
        return str(obj.pokemon)

    class Meta:
        model = CaughtPokemon
        fields = ['id', 'owner', 'profile_id', 'is_owner',
                  'profile_image', 'pokemon', 'pokemon_name'
                  ]
