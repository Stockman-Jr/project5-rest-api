import json
import requests

items_list = []


poke_response = requests.get(f"https://pokeapi.co/api/v2/item-attribute/7")

item = poke_response.json()

held_items = []
for itm in item["items"]:
    held_items.append({"name": itm["name"]})

items_list.append(
    {
        "items": held_items

    }
)

print("succefully added all items!")


with open("helditems.json", "w") as outfile:
    json.dump(items_list, outfile, indent=2)
