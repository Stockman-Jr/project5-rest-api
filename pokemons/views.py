from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_api.permissions import IsOwnerOrReadOnly
from rest_api.pagination import CustomPokemonPagination
from .models import Pokemon, CaughtPokemon, Nature, HeldItem
from rest_framework import permissions, viewsets, filters
from rest_framework.response import Response


class NatureViewSet(viewsets.ModelViewSet):
    queryset = Nature.objects.all()
    serializer_class = NatureSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class HeldItemViewSet(viewsets.ModelViewSet):
    queryset = HeldItem.objects.all()
    serializer_class = HeldItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    pagination_class = CustomPokemonPagination
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
    queryset = CaughtPokemon.objects.all().order_by('-created_at')
    serializer_class = CaughtPokemonSerializer
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

    def get_serializer_class(self):
        if self.action == 'create':
            return CaughtPokemonCreateSerializer
        return super().get_serializer_class()

    def create(self, request):
        user = request.user
        pokemon = Pokemon.objects.get(pk=request.data['pokemon'])
        serializer = CaughtPokemonCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=user, pokemon=pokemon)
        return Response(serializer.data)
