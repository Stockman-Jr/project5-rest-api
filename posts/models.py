from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from pokemons.models import CaughtPokemon, Nature, HeldItem
from model_utils.managers import InheritanceManager


GAME_CHOICES = [
        ('pokemon_scarlet', 'Pokémon Scarlet'),
        ('pokemon_violet', 'Pokémon Violet'),
        ('pokemon_arceus', 'Pokémon Legends: Arceus'),
        ('pokemon_bd', 'Pokémon Brilliant Diamond'),
        ('pokemon_sp', 'Pokémon Shining Pearl'),
        ('pokemon_sword', 'Pokémon Sword'),
        ('pokemon_shield', 'Pokémon Shield'),
        ('pokemon_lets_go_eevee', 'Pokémon Lets Go Eeevee'),
        ('pokemon_lets_go_pikachu', 'Pokémon Lets Go Pikachu'),
        ('pokemon_go', 'Pokémon GO'),
        ('other', 'Other'),
    ]

EV_CHOICE_STATS = [
        ('hp', 'HP'),
        ('attack', 'Attack'),
        ('defense', 'Defense'),
        ('special_attack', 'Special Attack'),
        ('special_defense', 'Special Defense'),
        ('speed', 'Speed'),
    ]


class BasePost(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True)
    post_type = models.CharField(max_length=100)
    game_filter = models.CharField(
        max_length=32, choices=GAME_CHOICES, default=''
    )
    objects = InheritanceManager()

    def __str__(self):
        return f"{self.post_type} {self.id}"


class Post(BasePost):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', blank=True)
    ingame_name = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id} {self.title}"


class PokemonBuild(BasePost):
    pokemon = models.ForeignKey(
        CaughtPokemon, related_name='pokemons_caught', on_delete=models.CASCADE
        )
    move_one = models.CharField(max_length=100)
    move_two = models.CharField(max_length=100)
    move_three = models.CharField(max_length=100)
    move_four = models.CharField(max_length=100)
    ability = models.CharField(max_length=100)
    nature = models.ForeignKey(Nature, on_delete=models.CASCADE)
    held_item = models.ForeignKey(HeldItem, on_delete=models.CASCADE)
    ev_stats = MultiSelectField(
        max_length=100, max_choices=2, choices=EV_CHOICE_STATS, default=''
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s {self.pokemon} build"
