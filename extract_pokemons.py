import json
import requests

#############################################
# Extracts data from pokeapi to a json file #
#############################################

pokemon_list = []

ITERATOR = 1

while True:
    poke_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{ITERATOR}")

    if poke_response.status_code != 200:
        print("No more pokemons!")
        break

    pokemon = poke_response.json()

    poke_id = str(pokemon["id"]).zfill(3)
    poke_name = pokemon["name"]
    poke_types = [e["type"]["name"] for e in pokemon["types"]]
    poke_abilities = [e["ability"]["name"] for e in pokemon["abilities"]]
    poke_moves = [e["move"]["name"] for e in pokemon["moves"]]

    pokemon_list.append(
        {
            "id": poke_id,
            "name": poke_name,
            "sprite": f"https://assets.pokemon.com/assets/cms2/img/pokedex/detail/{poke_id}.png",
            "types": poke_types,
            "abilities": poke_abilities,
            "moves": poke_moves,

        }
    )

    print(f"id:{poke_id} name:{poke_name} succefully added!")
    ITERATOR += 1

with open("pokedata.json", "w") as outfile:
    json.dump(pokemon_list, outfile, indent=2)
