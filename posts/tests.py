from django.contrib.auth.models import User
from .models import BasePost, Post, PokemonBuild
from pokemons.models import Pokemon, CaughtPokemon, Nature, HeldItem
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):

    def setUp(self):
        lily = User.objects.create_user(username='lily', password='pass')
        self.client.login(username='lily', password='pass')
        poke = Pokemon.objects.create(name="pidgey")
        caught_pokemon = CaughtPokemon.objects.create(pokemon=poke, owner=lily)
        HeldItem.objects.create(name="leftovers")
        Nature.objects.create(name="hardy")

    def test_can_list_all_posts(self):
        lily = User.objects.get(username='lily')
        Post.objects.create(
            owner=lily, title='test title', post_type='Game Content'
            )
        item = HeldItem.objects.create(name="leftovers")
        nature = Nature.objects.create(name="hardy")
        caught_pokemon = CaughtPokemon.objects.get(id=1)
        PokemonBuild.objects.create(
            owner=lily, pokemon=caught_pokemon, held_item=item,
            nature=nature, post_type="Pokemon Build"
            )
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)
        # print(len(response.data))

    def test_can_list_posts(self):
        lily = User.objects.get(username='lily')
        Post.objects.create(owner=lily, title='test title')
        response = self.client.get('/posts/post/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_list_pokemon_build_posts(self):
        lily = User.objects.get(username='lily')
        item = HeldItem.objects.create(name="leftovers")
        nature = Nature.objects.create(name="hardy")
        caught_pokemon = CaughtPokemon.objects.get(id=1)
        PokemonBuild.objects.create(
            owner=lily, pokemon=caught_pokemon, held_item=item, nature=nature
            )
        response = self.client.get('/posts/pokebuild/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='lily', password='pass')
        response = self.client.post(
            '/posts/post/',
            {'title': 'test title', 'post_type': 'Game Content'}
            )
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cant_create_post(self):
        self.client.logout()
        response = self.client.post('/posts/post/', {
            'title': 'test title', 'post_type': 'Game Content'
            })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in_user_can_create_pokemon_build(self):
        self.client.login(username='lily', password='pass')
        response = self.client.post(
            '/posts/pokebuild/',
            {
             'pokemon': 1, 'held_item': 1, 'nature': 1,
             'post_type': 'Pokemon Build', 'move_one': 'slash',
             'move_two': 'fly', 'move_three': 'tackle',
             'move_four': 'calm mind', 'ability': 'ability'
             }
            )
        count = PokemonBuild.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # def test_logged_in_user_cant_create_pokemon_build(self):
        #    self.client.logout()
        #    response = self.client.post(
        #        '/posts/pokebuild/',
        #        {
        #         'pokemon': 1, 'held_item': 1, 'nature': 1,
        #         'post_type': 'Pokemon Build', 'move_one': 'slash',
        #         'move_two': 'fly', 'move_three': 'tackle',
        #         'move_four': 'calm mind', 'ability': 'ability'
        #        }
        #        )
        #    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        lily = User.objects.create_user(username='lily', password='pass')
        brian = User.objects.create_user(username='brian', password='pass')
        Post.objects.create(
            owner=lily, title='test title', content='lilys content'
        )
        Post.objects.create(
            owner=brian, title='another title', content='brians content'
        )
    
    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/post/1/')
        self.assertEqual(response.data['title'], 'test title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/post/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='lily', password='pass')
        response = self.client.put('/posts/post/1/', {'title': 'update test title', 'post_type': 'Game Content'})
        print(response.data)
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'update test title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_post(self):
        self.client.login(username='lily', password='pass')
        response = self.client.put('/posts/post/2/', {'title': 'update brians title', 'post_type': 'Game Content'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


