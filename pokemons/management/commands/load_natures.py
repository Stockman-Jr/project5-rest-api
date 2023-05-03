from django.core.management.base import BaseCommand
import json
from pokemons.models import Nature


class Command(BaseCommand):

    def load_nature_data(self, context):
        nature_obj = Nature.objects
        for nature in context['natures']:
            new_nature = nature_obj.create(
                name=nature['name']
            )

    def handle(self, *args, **options):
        with open('pokenatures.json') as f:
            context = json.load(f)
            self.load_nature_data(context)
