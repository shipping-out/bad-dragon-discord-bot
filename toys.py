import requests
from tabulate import tabulate

def get_inventory_toys(page, limit, types):
    all_toys = []

    for toyType in types:
        url = f"https://bad-dragon.com/api/inventory-toys?price[min]=0&price[max]=300&sort[field]=price&sort[direction]=asc&page={page}&limit={limit}&category={toyType}"
        response = requests.get(url)
        api_data = response.json()
        toys = api_data.get("toys", [])

        for toy in toys:
            price = toy["price"]
            sku = toy["sku"]
            original_price = toy["original_price"]
            color = toy["color_display"]
            is_flop = toy["is_flop"]
            external_flop_reason = toy.get("external_flop_reason")
            image_url = toy["images"][0]["imageUrlFull"] if toy["images"] else None

            all_toys.append([price, sku, original_price, color, is_flop, external_flop_reason, image_url])

    return all_toys

def create_masturbators(toy_types):
    table_data = get_inventory_toys(1, 60, toy_types)
    headers = ["Price", "Product Name", "Original Price", "Color", "Is Flop", "External Flop Reason", "Image URL"]
    return table_data, headers

def getToys(types):
    table_data, headers = create_masturbators(types)
    return table_data
