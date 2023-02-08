from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_api.permissions import IsOwnerOrReadOnly
from .serializers import TrainerProfileSerializer
from .models import TrainerProfile


class TrainerProfileList(generics.ListAPIView):

    queryset = TrainerProfile.objects.all()
    serializer_class = TrainerProfileSerializer


class TrainerProfileDetail(generics.RetrieveUpdateAPIView):

    permission_classes = [IsOwnerOrReadOnly]
    queryset = queryset = TrainerProfile.objects.all()
    serializer_class = TrainerProfileSerializer