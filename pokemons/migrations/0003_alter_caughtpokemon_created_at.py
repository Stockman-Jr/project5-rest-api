# Generated by Django 3.2.17 on 2023-02-12 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemons', '0002_caughtpokemon_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caughtpokemon',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]