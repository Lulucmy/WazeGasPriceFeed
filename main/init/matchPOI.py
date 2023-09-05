import json
import csv
import math
from config import Init

# Using Haversine formula to calculate distance between two points on a sphere
def haversine(lat1, lon1, lat2, lon2):
    R = 6356752
    lon1, lat1, lon2, lat2 = map(float, [lon1, lat1, lon2, lat2])
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# Using n-gram to calculate similarity between two station names
def ngram(sentence, num):
    tmp = [] 
    sent_len = len(sentence) - num +1
    for i in range(sent_len):
        tmp.append(sentence[i:i+num]) 
    return tmp

# Calculating similarity between names
def diff_ngram(sent_a, sent_b, num):
    a = ngram(sent_a, num)
    b = ngram(sent_b, num) 
    common = [] 
    cnt = 0 
    for i in a:
        for j in b:
            if i == j:
                cnt += 1
                common.append(i)
    return cnt/len(a)

# Calculating similarity between brands (to avoid matching different brands)
def matchbrands(brand1, brand2, name1, name2):
    brand1, brand2, name1, name2 = map(str.lower, [brand1, brand2, name1, name2])
    brand1_match = None
    brand2_match = None
    match = False
    
    for brand_list_name, brands in Init.__brandnames__.items():
        brand1_words = brand1.split()
        name1_words = name1.split()
        station1 = brand1_words + name1_words
        brand2_words = brand2.split()
        name2_words = name2.split()
        station2 = brand2_words + name2_words

        for i in station1:
            if i in brands:
                brand1_match = brand_list_name
                break
        for i in station2:
            if i in brands:
                brand2_match = brand_list_name
                break
        if (brand1_match == brand2_match) & (brand1_match != None) & (brand2_match != None):
            match = True
            break   
    return match

# Matching POIs with stations
def match_pois_with_stations(pois, stations):
    matched = []
    remain = []

    for poi in pois:
        min_distance = float('inf')
        nearest_station = None

        for uid, station in stations.items():
            station_lat, station_lon = station['coord']
            distance = haversine(poi['LAT'], poi['LONG'], station_lat, station_lon)

            if distance < min_distance:
                min_distance = distance
                nearest_station = uid

        if nearest_station:
            station = stations[nearest_station]
            if min_distance < 50 or (50 <= min_distance <= 100 and matchbrands(poi['BRAND'], station['brand'], poi['NAME'], station['name'])):
                matched.append({
                    nearest_station: {
                        "wazename": poi['BRAND']+ " " + poi['NAME'],
                        "gouvname": station['name']+ " " + station['brand'],
                        "venue_id": poi['VENUE_ID'],
                        "coord": [poi['LAT'], poi['LONG']],
                        "link": poi['PERMALINK'],
                        "author": "autoimport"
                    }
                })
            else:
                remain.append(poi)
        else:
            remain.append(poi)
        print(f"{pois.__len__()} / {matched.__len__()}", end='\r')

    return matched, remain


def main():
    with open('data/pois.csv', 'r') as csvfile:
        pois = list(csv.DictReader(csvfile, delimiter=';'))

    with open('data/export.json', 'r') as jsonfile:
        stations = json.load(jsonfile)

    matched, remain = match_pois_with_stations(pois, stations)

    with open('data/output.json', 'w') as outputfile:
        json.dump(matched, outputfile, indent=4)

    with open('remain.csv', 'w', newline='') as remainfile:
        fieldnames = ["LAT", "LONG", "STREET", "NAME", "BRAND", "VENUE_ID", "PERMALINK"]
        writer = csv.DictWriter(remainfile, fieldnames=fieldnames)
        writer.writeheader()
        for poi in remain:
            writer.writerow(poi)

if __name__ == "__main__":
    main()
