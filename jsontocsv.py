import json
import csv

def json_to_csv(json_file, csv_file):
    # Load data from the JSON file
    with open(json_file, 'r', encoding='utf-8') as jf:
        data = json.load(jf)
    
    # Ensure the JSON data is a list of dictionaries
    if not isinstance(data, list) or not data:
        print("JSON file should contain a non-empty list of dictionaries.")
        return

    # Get the CSV header from the keys of the first dictionary
    header = data[0].keys()

    # Write the data to a CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as cf:
        writer = csv.DictWriter(cf, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)

    print(f"Converted {json_file} to {csv_file} successfully.")

if __name__ == "__main__":
    json_file = "results.json"   # Replace with your JSON file name
    csv_file = "FinalOutput.csv"    # Desired CSV file name
    json_to_csv(json_file, csv_file)
