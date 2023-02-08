import json
import requests

natures_list = []
ITERATOR = 1

while True:
    poke_response = requests.get(f"https://pokeapi.co/api/v2/nature/{ITERATOR}")

    if poke_response.status_code != 200:
        print("nothing more to add")
        break

    pokemon = poke_response.json()

    natures_list.append(
        {
            "name": pokemon["name"]
        }
    )

    ITERATOR += 1


with open("pokenatures.json", "w") as outfile:
    json.dump(natures_list, outfile, indent=2)
