from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from .models import Pokemon, CaughtPokemon
from rest_framework import permissions, viewsets, filters
from rest_framework.response import Response


class PokemonListView(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    search_fields = [
        'name',
        'types__name',
    ]

    ordering_fields = [
        'id',
        'name',
    ]


class AddCaughtPokemonView(viewsets.ModelViewSet):
    queryset = CaughtPokemon.objects.all()
    serializer_class = CaughtPokemonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = [
        'id',
        'pokemon__name',
    ]

    search_fields = [
        'pokemon__name',
    ]
    # .order_by('-created_at')
    def get_queryset(self):
        user = self.request.user
        return CaughtPokemon.objects.filter(owner=user)

    def create(self, request):
        user = request.user
        pokemon = Pokemon.objects.get(pk=request.data['pokemon'])
        serializer = CaughtPokemonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=user, pokemon=pokemon)
        return Response(serializer.data)
