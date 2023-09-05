import re
import json
import time
import requests
from config import Stats

#from config import Stats
def build(output_data):
    gas_prices = output_data["gas_prices"]
    
    gas_price_count = {}  # To store the count of gas prices for each gas type
    gas_price_total = {}  # To store the total price of gas for each gas type
    
    station_count = 0
    
    for entry in gas_prices:
        station_count += 1
        
        for price in entry["prices"]:
            gas_name = price["name"]
            gas_price = price["price"]
            
            if gas_name not in gas_price_count:
                gas_price_count[gas_name] = 1
                gas_price_total[gas_name] = gas_price
            else:
                gas_price_count[gas_name] += 1
                gas_price_total[gas_name] += gas_price
    
    gas_price_avg = {gas_name: gas_price_total[gas_name] / gas_price_count[gas_name] for gas_name in gas_price_count}
    
    statistics_data = {
        "average_gas_prices": gas_price_avg,
        "number_of_stations": station_count
    }
    
    return statistics_data

def writewebhook(statistics_data):
    with open("main/utils/webhook.json", mode="r") as json_file:
        data = json.load(json_file)

    replacements = {
        "{nbstations}": str(statistics_data["number_of_stations"]),
        "{pmoygazole}": "{:.2f}".format(float(statistics_data["average_gas_prices"].get("gazole", "N/A"))),
        "{pmoye85}": "{:.2f}".format(float(statistics_data["average_gas_prices"].get("98", "N/A"))),
        "{pmoye10}": "{:.2f}".format(float(statistics_data["average_gas_prices"].get("95", "N/A")))
    }

    for key, value in replacements.items():
        for i, embed in enumerate(data["embeds"]):
            data["embeds"][i]["description"] = embed["description"].replace(key, value)
            for j, field in enumerate(embed["fields"]):
                data["embeds"][i]["fields"][j]["value"] = field["value"].replace(key, value)

    return data


def sendwebhook(statistics_data):
    with open("data/lastsent.json", mode="r") as jsontime:
        jsonts = json.load(jsontime)
    data = writewebhook(statistics_data)
    if float(jsonts["timestamp"]) + 86300 <= time.time():
        result = requests.post(Stats.__extURL__, json=data)
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            print("Payload delivered successfully, code {}.".format(result.status_code))
            jsonts["timestamp"] = time.time()
            with open("data/lastsent.json", mode="w") as jsontime:
                json.dump(jsonts, jsontime)
    else:
        print("Webhook already sent today.")
    requests.post(Stats.__intURL__, json=data)