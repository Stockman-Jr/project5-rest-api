from .serializers import *
from .models import Pokemon
from rest_framework import generics, permissions


class PokemonListView(generics.ListAPIView):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
