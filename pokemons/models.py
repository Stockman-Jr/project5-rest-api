from django.db import models


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
