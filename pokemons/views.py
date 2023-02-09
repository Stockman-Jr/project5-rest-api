from .serializers import *
from .models import Pokemon, CaughtPokemon
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response


class PokemonListView(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AddCaughtPokemonView(viewsets.ModelViewSet):
    queryset = CaughtPokemon.objects.all()
    serializer_class = CaughtPokemonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request):
        user = request.user
        pokemon = Pokemon.objects.get(pk=request.data['pokemon'])
        serializer = CaughtPokemonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=user, pokemon=pokemon)
        return Response(serializer.data)
