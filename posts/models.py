from django.db import models
from django.contrib.auth.models import User


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
