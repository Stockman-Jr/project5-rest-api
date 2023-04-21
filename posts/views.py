from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_api.permissions import IsOwnerOrReadOnly
from .models import BasePost, Post, PokemonBuild
from .serializers import *
from likes.models import Like
from .filters import PokeBuildGameFilter, PostGameFilter, AllPostGameFilter
from rest_framework.response import Response


class AllPostsListView(generics.ListAPIView):
    serializer_class = AllPostsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend,]

    filterset_class = AllPostGameFilter

    def get_queryset(self):
        return BasePost.objects.select_subclasses()


class PostListView(generics.ListCreateAPIView):

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    filterset_class = PostGameFilter

    filterset_fields = [
        'owner__trainerprofile',
        'likes_count',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
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

    filterset_class = PokeBuildGameFilter

    filterset_fields = [
        'owner__trainerprofile',
        'likes_count',
    ]

    search_fields = [
        'owner__username',
    ]

    ordering_fields = [
        'comments_count',
        'likes_count',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PokeBuildDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = PokeBuildSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = PokemonBuild.objects.all()
