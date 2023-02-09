from django.urls import path
from pokemons import views


urlpatterns = [
    path('pokemons/', views.PokemonListView.as_view()),
]