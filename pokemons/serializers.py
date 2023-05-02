from rest_framework import serializers
from .models import Pokemon, CaughtPokemon, Nature, HeldItem


class HeldItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeldItem
        fields = ['id', 'name']


class NatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nature
        fields = ['id', 'name']


class PokemonSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()
    types = serializers.StringRelatedField(many=True, read_only=True)
    sprite = serializers.StringRelatedField(read_only=True)
    abilities = serializers.StringRelatedField(many=True, read_only=True)
    moves = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Pokemon
        fields = '__all__'


class PokemonListSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()
    types = serializers.StringRelatedField(many=True, read_only=True)
    sprite = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Pokemon
        fields = ['id', 'name', 'sprite', 'types']


class CaughtPokemonCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CaughtPokemon
        fields = ['id', 'pokemon']


class CaughtPokemonDetailSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    pokemon = PokemonSerializer()

    class Meta:
        model = CaughtPokemon
        fields = ['id', 'owner', 'pokemon']
        depth = 1


class CaughtPokemonSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    profile_id = serializers.ReadOnlyField(source='owner.trainerprofile.id')
    pokemon = PokemonListSerializer()

    class Meta:
        model = CaughtPokemon
        fields = ['id', 'owner', 'profile_id', 'pokemon', 'created_at']
