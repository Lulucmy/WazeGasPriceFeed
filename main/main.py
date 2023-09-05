import json
import time
from utils import fetch, match, stats

if __name__ == "__main__":
    start = time.time()
    #Initialize output data
    output_data = {"gas_prices": []}

    #Fetch prices from government feed
    root = fetch.pricedata()

    #Fetch stations from Sheets API
    reader = fetch.stationdata()

    #Match prices and stations
    output_data = match.stations(output_data, reader, root)

    #Write output to file
    with open('fuel.json', 'w') as output_file:
        json.dump(output_data, output_file, indent=4)
    
    #Sending statistics
    statdata = stats.build(output_data)
    stats.sendwebhook(statdata)

    #Return elapsed time
    end = time.time()
    print(f"Completed in {float(end-start)} seconds")
    