from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_api.permissions import IsOwnerOrReadOnly
from .serializers import TrainerProfileSerializer
from .models import TrainerProfile


class TrainerProfileList(generics.ListAPIView):

    queryset = TrainerProfile.objects.annotate(
        posts_count=Count('owner__basepost', distinct=True),
        pokemons_count=Count('owner__caughtpokemon', distinct=True)
    ).order_by('-created_at')
    serializer_class = TrainerProfileSerializer
    filter_backends = [filters.OrderingFilter]

    ordering_fields = [
        'posts_count',
        'pokemons_count'
    ]


class TrainerProfileDetail(generics.RetrieveUpdateAPIView):

    permission_classes = [IsOwnerOrReadOnly]
    queryset = queryset = TrainerProfile.objects.annotate(
        posts_count=Count('owner__basepost', distinct=True),
        pokemons_count=Count('owner__caughtpokemon', distinct=True)
    ).order_by('-created_at')
    serializer_class = TrainerProfileSerializer
