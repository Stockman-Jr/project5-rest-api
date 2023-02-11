from django_filters import rest_framework as filters
from .models import PokemonBuild, Post, BasePost, GAME_CHOICES


class BaseGameFilter(filters.FilterSet):
    game_filter = filters.ChoiceFilter(choices=GAME_CHOICES)


class AllPostGameFilter(BaseGameFilter):
    class Meta:
        model = BasePost
        fields = ['game_filter']


class PostGameFilter(BaseGameFilter):
    class Meta:
        model = Post
        fields = ['game_filter']


class PokeBuildGameFilter(BaseGameFilter):
    class Meta:
        model = PokemonBuild
        fields = ['game_filter']

