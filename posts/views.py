from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_api.permissions import IsOwnerOrReadOnly
from .models import BasePost, Post, PokemonBuild
from .serializers import AllPostsSerializer, PostSerializer, PokeBuildSerializer
from likes.models import Like


class AllPostsListView(generics.ListAPIView):
    serializer_class = AllPostsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return BasePost.objects.select_subclasses()


class PostListView(generics.ListCreateAPIView):

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()


class PokeBuildListView(generics.ListCreateAPIView):

    serializer_class = PokeBuildSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = PokemonBuild.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    search_fields = [
        'owner__username',
        'pokemon__name',
    ]

    ordering_fields = [
        'comments_count',
        'likes_count',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PokeBuildDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = PokeBuildSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = PokemonBuild.objects.all()
