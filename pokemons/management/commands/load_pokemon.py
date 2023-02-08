from django.core.management.base import BaseCommand
import json
from pokemons.models import Pokemon, Ability, Move, Type


class Command(BaseCommand):
    help = 'Load JSON pokemon pokemon'

    def get_or_create_abilities(self, abilities):
        abilities_obj = Ability.objects
        abilities_id = []

        for ability in abilities:
            if abilities_obj.filter(name=ability):
                for i in abilities_obj.filter(name=ability):
                    abilities_id.append(i)
            else:
                abilities_obj.create(name=ability)
                for i in abilities_obj.filter(name=ability):
                    abilities_id.append(i)
        return abilities_id

    def get_or_create_moves(self, moves):
        moves_obj = Move.objects
        moves_id = []
        for move in moves:
            if moves_obj.filter(name=move):
                for i in moves_obj.filter(name=move):
                    moves_id.append(i)
            else:
                moves_obj.create(name=move)
                for i in moves_obj.filter(name=move):
                    moves_id.append(i)
        return moves_id
    
    def get_or_create_types(self, types):
        types_obj = Type.objects
        types_id = []
        for type in types:
            if types_obj.filter(name=type):
                for i in types_obj.filter(name=type):
                    types_id.append(i)
            else:
                types_obj.create(name=type)
                for i in types_obj.filter(name=type):
                    types_id.append(i)
        return types_id

    def load_pokemon_data(self, context):
        pokemon_obj = Pokemon.objects
        for pokemon in context['pokemon']:
            new_pokemon = pokemon_obj.create(
                name=pokemon['name'],
                sprite=pokemon['sprite'],
            )
            new_pokemon = pokemon_obj.get(pk=new_pokemon.id)

            abilities = self.get_or_create_abilities(pokemon['abilities'])
            if abilities:
                for ability in abilities:
                    if not new_pokemon.abilities.filter(pk=ability.id):
                        new_pokemon.abilities.add(ability.id)

            moves = self.get_or_create_moves(pokemon['moves'])
            if moves:
                for move in moves:
                    if not new_pokemon.moves.filter(pk=move.id):
                        new_pokemon.moves.add(move.id)

            types = self.get_or_create_types(pokemon['types'])
            if types:
                for type in types:
                    if not new_pokemon.types.filter(pk=type.id):
                        new_pokemon.types.add(type.id)

    def handle(self, *args, **options):
        with open('pokedata.json') as f:
            context = json.load(f)
            self.load_pokemon_data(context)