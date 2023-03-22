from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_api.permissions import IsOwnerOrReadOnly
from rest_api.pagination import CustomPagination
from .models import Pokemon, CaughtPokemon
from rest_framework import permissions, viewsets, filters
from rest_framework.response import Response


class PokemonListView(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    pagination_class = CustomPagination
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
    action_serializers = {
        'retrieve': CaughtPokemonDetailSerializer,
        'list': CaughtPokemonSerializer,
        'create': CaughtPokemonSerializer
    }
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

    def get_serializer_class(self):

        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(
                self.action, self.serializer_class
                )

        return super(AddCaughtPokemonView, self).get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        return CaughtPokemon.objects.filter(owner=user).order_by('-created_at')

    def create(self, request):
        user = request.user
        pokemon = Pokemon.objects.get(pk=request.data['pokemon'])
        serializer = CaughtPokemonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=user, pokemon=pokemon)
        return Response(serializer.data)
