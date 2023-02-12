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
    pokemon_name = serializers.SerializerMethodField()

    def get_pokemon_name(self, obj):
        return str(obj.pokemon)

    class Meta:
        model = CaughtPokemon
        fields = ['id', 'owner', 'pokemon', 'pokemon_name']
        depth = 1


class CaughtPokemonSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    pokemon_name = serializers.SerializerMethodField()

    def get_pokemon_name(self, obj):
        return str(obj.pokemon)

    class Meta:
        model = CaughtPokemon
        fields = ['id', 'owner', 'pokemon', 'pokemon_name']