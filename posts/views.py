from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import (
     DjangoFilterBackend, FilterSet, CharFilter, ChoiceFilter
    )
from rest_api.permissions import IsOwnerOrReadOnly
from rest_api.pagination import CustomPostPagination
from .models import BasePost, Post, PokemonBuild
from .serializers import *
from likes.models import Like
from rest_framework.response import Response


class CustomPostFilter(FilterSet):
    post_category = CharFilter(
        method='filter_post_category', lookup_expr='exact'
        )

    class Meta:
        model = BasePost
        fields = ('post_category', 'owner__trainerprofile',
                  'likes__owner__trainerprofile',)

    def filter_post_category(self, queryset, name, value):
        if value == 'post':
            queryset = queryset.filter(post__isnull=False)
        elif value == 'pokebuild':
            queryset = queryset.filter(pokemonbuild__isnull=False)
        return queryset


class AllPostsListView(generics.ListAPIView):
    serializer_class = AllPostsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = CustomPostPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
        ]

    filterset_class = CustomPostFilter

    ordering_fields = [
        'comments_count',
        'likes_count',
    ]

    search_fields = [
        'game_filter',
        'owner__username',
    ]

    def get_queryset(self):
        return BasePost.objects.select_subclasses().annotate(
            comments_count=Count('comment', distinct=True),
            likes_count=Count('likes', distinct=True),
        ).order_by('-created_at')


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

    filterset_fields = [
        'owner__trainerprofile',
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

    filterset_fields = [
        'owner__trainerprofile',
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
    queryset = PokemonBuild.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    )
