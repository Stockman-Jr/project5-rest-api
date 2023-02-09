from django.db import models
from django.contrib.auth.models import User


class Ability(models.Model):
    name = models.CharField('name', max_length=100)

    def __str__(self):
        return f'{self.name}'


class Move(models.Model):
    name = models.CharField('name', max_length=100)

    def __str__(self):
        return f'{self.name}'


class Type(models.Model):
    name = models.CharField('name', max_length=100)

    def __str__(self):
        return f'{self.name}'


class Nature(models.Model):
    name = models.CharField('name', max_length=100)

    def __str__(self):
        return f'{self.name}'


class HeldItem(models.Model):
    name = models.CharField('name', max_length=100)

    def __str__(self):
        return f'{self.name}'


class Pokemon(models.Model):
    name = models.CharField('name', max_length=100)
    sprite = models.CharField('name', max_length=1200)
    types = models.ManyToManyField(Type, related_name='types')
    abilities = models.ManyToManyField(Ability, related_name='abilities')
    moves = models.ManyToManyField(Move, related_name='moves')

    def __str__(self):
        return f'{self.name}'


class CaughtPokemon(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    pokemon = models.ForeignKey(
        Pokemon, related_name='pokemons', on_delete=models.CASCADE
        )

    def __str__(self):
        return f'{self.pokemon.name}'

