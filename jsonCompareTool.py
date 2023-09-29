import json
from prettytable import PrettyTable

def compare_json_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        json_data1 = json.load(f1)
        json_data2 = json.load(f2)

    differences = compare_json_objects(json_data1, json_data2)

    return differences

def compare_json_objects(obj1, obj2, path=""):
    differences = []

    if type(obj1) != type(obj2):
        differences.append((path, str(obj1), str(obj2), "Different"))
        return differences

    if isinstance(obj1, dict):
        if set(obj1.keys()) != set(obj2.keys()):
            differences.append((path, json.dumps(obj1), json.dumps(obj2), "Different"))
        for key in obj1:
            new_path = f"{path}.{key}" if path else key
            differences.extend(compare_json_objects(obj1[key], obj2[key], new_path))
    elif isinstance(obj1, list):
        if len(obj1) != len(obj2):
            differences.append((path, json.dumps(obj1), json.dumps(obj2), "Different"))
        for i, (item1, item2) in enumerate(zip(obj1, obj2)):
            new_path = f"{path}[{i}]"
            differences.extend(compare_json_objects(item1, item2, new_path))
    else:
        if obj1 != obj2:
            differences.append((path, str(obj1), str(obj2), "Different"))
        else:
            differences.append((path, str(obj1), str(obj2), "Same"))

    return differences

def list_columns(differences):
    columns = set()
    for diff in differences:
        columns.add(diff[0])  # Extracting the path (column name)
    return columns

def main():
    file1 = 'before.json'
    file2 = 'after.json'

    differences = compare_json_files(file1, file2)

    if not differences:
        print("No differences found")
    else:
        print("Differences found:")
        table = PrettyTable()
        table.field_names = ["Path", "Before", "After", "Difference"]
        for diff in differences:
            table.add_row(diff)
        print(table)

        # List unique columns (paths)
        columns = list_columns(differences)
        print("\nColumns in the differences:")
        for column in columns:
            for diff in differences:
                if diff[0] == column and diff[3] == "Different":
                    print(column)
                    break

if __name__ == "__main__":
    main()