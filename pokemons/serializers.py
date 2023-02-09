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


class CaughtPokemonSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = CaughtPokemon
        fields = ['id', 'owner', 'pokemon']