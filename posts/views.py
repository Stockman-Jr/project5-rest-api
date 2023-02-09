from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_api.permissions import IsOwnerOrReadOnly
from .models import Post, PokemonBuildPost
from .serializers import PostSerializer, PostPokeBuildSerializer


class PostListView(generics.ListCreateAPIView):

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()


class PokeBuildListView(generics.ListCreateAPIView):
    serializer_class = PostPokeBuildSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = PokemonBuildPost.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PokeBuildDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostPokeBuildSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = PokemonBuildPost.objects.all()
