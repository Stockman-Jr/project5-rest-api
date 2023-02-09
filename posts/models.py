from django.db import models
from django.contrib.auth.models import User
from pokemons.models import CaughtPokemon, Nature, HeldItem


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


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank=True)
    ingame_name = models.CharField(max_length=255, blank=True)
    game_filter = models.CharField(
        max_length=32, choices=GAME_CHOICES, default=''
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id} {self.title}"


class PokemonBuildPost(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
        )
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
    ev_stats = models.CharField(
        max_length=100, choices=EV_CHOICE_STATS, default=''
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    game_filter = models.CharField(
        max_length=32, choices=GAME_CHOICES, default=''
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s {self.pokemon} build"
