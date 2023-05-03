from django.core.management.base import BaseCommand
import json
from pokemons.models import HeldItem


class Command(BaseCommand):

    def load_items_data(self, context):
        item_obj = HeldItem.objects
        for item in context['items']:
            new_item = item_obj.create(
                name=item['name']
            )

    def handle(self, *args, **options):
        with open('helditems.json') as f:
            context = json.load(f)
            self.load_items_data(context)
