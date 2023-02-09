from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


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
