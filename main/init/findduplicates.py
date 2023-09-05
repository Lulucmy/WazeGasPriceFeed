import json
import csv

# Find duplicates in the data
def find_duplicates(data):
    duplicates = {}
    seen_numbers = set()

    for entry in data:
        for number in entry:
            if number in seen_numbers:
                if number not in duplicates:
                    duplicates[number] = []
                duplicates[number].append(entry[number])
            else:
                seen_numbers.add(number)

    return duplicates

# Output duplicates to file
def write_duplicates_to_file(duplicates):
    with open('result.txt', 'w') as f:
        for number, entries in duplicates.items():
            f.write(f'Duplicate entries for number: {number}\n')
            for entry in entries:
                f.write(json.dumps(entry, indent=4))
                f.write('\n')
            f.write('\n')

# Remove duplicates from CSV file (if needed)
def remove_dups():
    with open('poi_latest.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',')
        venue_ids = set()
        duplicates = set()
        for row in reader:
            venue_id = row[1]
            if venue_id in venue_ids:
                duplicates.add(venue_id)
            else:
                venue_ids.add(venue_id)

        if len(duplicates) > 0:
            print("Duplicates found: ", duplicates)
        else:
            print("No duplicates found.")

if __name__ == '__main__':
    with open('data/output.json', 'r') as json_file:
        data = json.load(json_file)

    duplicates = find_duplicates(data)
    write_duplicates_to_file(duplicates)

    print('Duplicate entries have been written to result.txt')

