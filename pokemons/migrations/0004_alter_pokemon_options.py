# Generated by Django 3.2.17 on 2024-09-09 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemons', '0003_alter_caughtpokemon_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pokemon',
            options={'ordering': ['id']},
        ),
    ]
