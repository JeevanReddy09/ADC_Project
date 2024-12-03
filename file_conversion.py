import json

# Load the dataset
with open("rows.json", "r") as file:
    raw_data = json.load(file)

# Extract metadata (columns) and data rows
columns = raw_data["meta"]["view"]["columns"]
rows = raw_data["data"]

# Map column names to row values
formatted_data = []
for row in rows:
    document = {}
    for i, col in enumerate(columns):
        column_name = col["fieldName"]  # Get the column name
        document[column_name] = row[i]  # Map column name to row value
    formatted_data.append(document)

# Save the formatted data to a new JSON file
with open("formatted_ev_data.json", "w") as outfile:
    json.dump(formatted_data, outfile, indent=4)

print("Data has been formatted successfully.")