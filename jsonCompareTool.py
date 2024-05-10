import json
import csv
from prettytable import PrettyTable

def compare_json_files(file1, file2, sort_key, ignore_keys):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        json_data1 = json.load(f1)  # Expecting a list of JSON objects
        json_data2 = json.load(f2)  # Expecting a list of JSON objects

    # Sort data by using a default value that sorts properly if key is missing
    json_data1.sort(key=lambda x: x.get('tradeReport', {}).get(sort_key, float('inf')))
    json_data2.sort(key=lambda x: x.get('tradeReport', {}).get(sort_key, float('inf')))

    differences = []
    ignored_differences = []
    # Ensure both files have the same number of JSON objects
    if len(json_data1) != len(json_data2):
        raise ValueError("The number of JSON objects in each file does not match.")

    for obj1, obj2 in zip(json_data1, json_data2):
        sequence_number = obj1.get('tradeReport', {}).get(sort_key, 'N/A')
        diffs, ignored = compare_json_objects(obj1, obj2, ignore_keys, sequence_number=sequence_number)
        differences.extend(diffs)
        ignored_differences.extend(ignored)

    return differences, ignored_differences

def compare_json_objects(obj1, obj2, ignore_keys, path="", sequence_number='N/A'):
    differences = []
    ignored_differences = []

    if isinstance(obj1, dict) and isinstance(obj2, dict):
        for key in set(obj1.keys()).union(obj2.keys()):
            if key in ignore_keys:
                ignored_differences.append((sequence_number, path + '.' + key if path else key, str(obj1.get(key)), str(obj2.get(key)), "Expected Difference"))
                continue
            new_path = f"{path}.{key}" if path else key
            diffs, ignored = compare_json_objects(obj1.get(key), obj2.get(key), ignore_keys, new_path, sequence_number)
            differences.extend(diffs)
            ignored_differences.extend(ignored)
    elif isinstance(obj1, list) and isinstance(obj2, list):
        for i, (item1, item2) in enumerate(zip(obj1, obj2)):
            new_path = f"{path}[{i}]"
            diffs, ignored = compare_json_objects(item1, item2, ignore_keys, new_path, sequence_number)
            differences.extend(diffs)
            ignored_differences.extend(ignored)
    else:
        if obj1 != obj2:
            differences.append((sequence_number, path, str(obj1), str(obj2), "Different"))

    return differences, ignored_differences

def main():
    file1 = 'old.json'
    file2 = 'new.json'
    sort_key = "sequenceNumber"  # Make sure this matches the actual key in your JSON
    ignore_keys_input = input("Enter keys to ignore in the comparison (comma separated): ")
    ignore_keys = {key.strip() for key in ignore_keys_input.split(',')}

    differences, ignored_differences = compare_json_files(file1, file2, sort_key, ignore_keys)

    if not differences and not ignored_differences:
        print("No differences found.")
    else:
        if differences:
            print("Comparison Results:")
            table = PrettyTable()
            table.field_names = ["Sequence Number", "Destinations", "Old", "New", "Status"]
            for diff in differences:
                table.add_row(diff)
            print(table)

        if ignored_differences:
            print("Ignored Differences:")
            ignored_table = PrettyTable()
            ignored_table.field_names = ["Sequence Number", "Destinations", "Old", "New", "Status"]
            for diff in ignored_differences:
                ignored_table.add_row(diff)
            print(ignored_table)

        # Save results into CSV
        csv_filename = "differences.csv"
        ignored_csv_filename = "ignored_differences.csv"
        with open(csv_filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Sequence Number", "Destinations", "Old", "New", "Status"])
            for diff in differences:
                csv_writer.writerow(diff)
        with open(ignored_csv_filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Sequence Number", "Destinations", "Old", "New", "Status"])
            for diff in ignored_differences:
                csv_writer.writerow(diff)
        print(f"Comparison results have been saved to {csv_filename}")
        print(f"Ignored differences have been saved to {ignored_csv_filename}")

if __name__ == "__main__":
    main()