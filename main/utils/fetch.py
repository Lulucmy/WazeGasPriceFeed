import csv
import requests
import zipfile
from io import BytesIO, StringIO
import xml.etree.ElementTree as ET
from config import URL

# Fetching functions 
## Get data from the government source & extract the zip
def pricedata() -> ET.Element:
    response = requests.get(URL.__govURL__)
    zip_file = zipfile.ZipFile(BytesIO(response.content))
    xml_file = zip_file.open("PrixCarburants_instantane.xml")
    tree = ET.parse(xml_file)
    root = tree.getroot()
    print("Fetched prices from governement")
    return root

## Get the latest stations data from the sheets
def stationdata() -> csv.DictReader:
    response = requests.get(URL.__stationsURL__)
    
    if response.status_code == 200:
        csv_data = response.content.decode('utf-8')
        reader = csv.DictReader(StringIO(csv_data)) 
        stations_data = {}
        for row in reader:
            station_id = row["stationid"]
            stations_data[station_id] = {
                "venueid": row["venue_id"],
                "location": [
                    float(row["lat"]),
                    float(row["lon"])
                ]
            }
        print("Fetched stations from Sheets")
    else:
        print("An error occured while fetching stations. Status code : " + str(response.status_code))
    
    return stations_data


# Test functions (to avoid fetching data from the internet)
## Get data from the government source (downloaded XML)
def pricedatatest() -> ET.Element:
    tree = ET.parse('data/pcitest.xml')
    root = tree.getroot()
    return root

## Get the stations data (downloaded CSV)
def stationdatatest() -> csv.DictReader:
    with open('data/poitest.csv', 'r') as csvfile:
        reader = list(csv.DictReader(csvfile, delimiter=','))
    stations_data = {}
    for row in reader:
        if row["stationid"].strip() and row["venue_id"].strip() and row["lat"].strip() and row["lon"].strip():
            station_id = row["stationid"]
            stations_data[station_id] = {
                "venueid": row["venue_id"],
                "location": [
                    float(row["lat"]),
                    float(row["lon"])
                ]
            }
        else:
            print("Invalid row detected.")
            continue
    return stations_data
