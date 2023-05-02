from .serializers import *
from django_filters.rest_framework import (
    DjangoFilterBackend, FilterSet, CharFilter
    )
from rest_api.permissions import IsOwnerOrReadOnly
from rest_api.pagination import CustomPokemonPagination
from .models import Pokemon, CaughtPokemon, Nature, HeldItem
from rest_framework import permissions, viewsets, filters
from rest_framework.response import Response


class CustomPokemonFilter(FilterSet):
    uncaught_pokemons = CharFilter(
        method='filter_uncaught_pokemons', lookup_expr='exact'
        )

    class Meta:
        model = Pokemon
        fields = ('uncaught_pokemons', 'types__name', 'pokemons__owner')

    def filter_uncaught_pokemons(self, queryset, name, value):
        if value.lower() == 'true' and self.request.user.is_authenticated:
            return queryset.filter(pokemons__owner__isnull=True)
        return queryset


class NatureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Nature.objects.all().order_by('id')
    serializer_class = NatureSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class HeldItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HeldItem.objects.all().order_by('id')
    serializer_class = HeldItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all().order_by('id')
    serializer_class = PokemonListSerializer
    pagination_class = CustomPokemonPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_class = CustomPokemonFilter

    search_fields = [
        'name',
        'types__name',
    ]

    ordering_fields = [
        'id',
        'name',
    ]


class AddCaughtPokemonView(viewsets.ModelViewSet):
    queryset = CaughtPokemon.objects.all().order_by('-created_at')
    serializer_class = CaughtPokemonSerializer
    pagination_class = CustomPokemonPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    filterset_fields = [
        'owner',
        'owner__trainerprofile',
        'pokemon__id',
    ]

    ordering_fields = [
        'id',
        'owner',
        'pokemon__name',
    ]

    search_fields = [
        'pokemon__name',
    ]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            self.permission_classes = [IsOwnerOrReadOnly, ]
        else:
            self.permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
        return super(AddCaughtPokemonView, self).get_permissions()

    def get_queryset(self):
        queryset = self.queryset
        pokemon_ids = self.request.GET.getlist('pokemon__in')
        if pokemon_ids:
            queryset = queryset.filter(pokemon__id__in=pokemon_ids)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return CaughtPokemonCreateSerializer
        if self.action == 'list':
            return CaughtPokemonSerializer
        elif self.action == 'retrieve':
            return CaughtPokemonDetailSerializer
        return super().get_serializer_class()

    def create(self, request):
        user = request.user
        pokemon = Pokemon.objects.get(pk=request.data['pokemon'])
        serializer = CaughtPokemonCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=user, pokemon=pokemon)
        return Response(serializer.data)
