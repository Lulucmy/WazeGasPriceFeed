from config import Feed
from datetime import datetime

#  Convert each date to timestamp and choose the most recent one
def timestamp(gas_price_entry) -> int:
    updated = int(max([datetime.strptime(price_elem.attrib['maj'], "%Y-%m-%d %H:%M:%S").timestamp() for price_elem in gas_price_entry.findall("./prix")]))
    return updated

#Convert gas prices
def pricelist(gas_price_entry):
    # Iterate over price elements
    prices = [
        {"name": Feed.gas_map.get(price_elem.attrib['nom'], price_elem.attrib['nom']), 
        "price": float(price_elem.attrib['valeur'])} 
        for price_elem in gas_price_entry.findall("./prix")]
    
    # Override the SP95 from the list if E10 is present, or convert it to E10
    if any(p["name"] == "SP95" for p in prices):
        if not any(p["name"] == "95" for p in prices):
            if Feed.overrideSP95:
                for p in prices:
                    if p["name"] == "SP95":
                        p["name"] = "95"
            else:
                prices = [p for p in prices if p["name"] != "SP95"]
        else:
            prices = [p for p in prices if p["name"] != "SP95"]
    prices = [p for p in prices if p["name"] != "SP98"]

    return prices

#Matching stations
def stations(output_data, stations_data, root):
    for station_id, station_info in stations_data.items():
        # Find the corresponding gas price entry in the XML
        gas_price_entry = root.find(f"./pdv[@id='{station_id}']")
        
        if (gas_price_entry is not None) and (gas_price_entry.findall("./prix")):
            # Build the station output entry
            entry = {
                "venue_id": station_info["venueid"],
                "location": station_info["location"],
                "updated": timestamp(gas_price_entry),
                "prices": pricelist(gas_price_entry)
            }
            
            # Add the entry to the output data
            output_data["gas_prices"].append(entry)
    print(f"Found {len(output_data['gas_prices'])} stations")
    return output_data
