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


class CaughtPokemonCreateSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = CaughtPokemon
        fields = ['id', 'owner', 'pokemon']


class CaughtPokemonSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    profile_id = serializers.ReadOnlyField(source='owner.trainerprofile.id')
    profile_avatar = serializers.ReadOnlyField(
        source='owner.trainerprofile.avatar.url'
        )
    pokemon = PokemonSerializer()

    class Meta:
        model = CaughtPokemon
        fields = ['id', 'owner', 'profile_id',
                  'profile_avatar', 'pokemon', 'created_at'
                  ]
        depth = 1
