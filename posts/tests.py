from django.contrib.auth.models import User
from .models import BasePost, Post, PokemonBuild
from pokemons.models import Pokemon, CaughtPokemon, Nature, HeldItem
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):

    def setUp(self):
        test = User.objects.create_user(username='test', password='pass')
        self.client.login(username='test', password='pass')
        poke = Pokemon.objects.create(name="pidgey")
        caught_pokemon = CaughtPokemon.objects.create(pokemon=poke, owner=test)

    def test_can_list_posts(self):
        test = User.objects.get(username='test')
        Post.objects.create(owner=test, title='test title')
        response = self.client.get('/posts/post/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_list_pokemon_build_posts(self):
        test = User.objects.get(username='test')
        item = HeldItem.objects.create(name="leftovers")
        nature = Nature.objects.create(name="hardy")
        caught_pokemon = CaughtPokemon.objects.get(id=1)
        PokemonBuild.objects.create(
            owner=test, pokemon=caught_pokemon, held_item=item, nature=nature
            )
        response = self.client.get('/posts/pokebuild/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

