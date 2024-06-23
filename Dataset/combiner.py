import csv
from collections import defaultdict

# Function to combine rows
def combine_rows(rows):
    combined = rows[0].copy()  # Start with the first row as a base
    for row in rows[1:]:
        for i in range(len(row)):
            if row[i] != '-' and not combined[i]:
                combined[i] = row[i]
    return combined

# Read the CSV file and combine rows
def combine_csv(input_file, output_file):
    combined_data = defaultdict(list)

    # Read the CSV file
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Read the header
        for row in reader:
            name = row[0]
            # Append each row to the corresponding name key
            combined_data[name].append([cell if cell != '-' else '' for cell in row])

    # Process and combine rows for each name
    merged_rows = []
    for name, rows in combined_data.items():
        merged_row = combine_rows(rows)
        merged_rows.append(merged_row)

    # Write the combined data to a new CSV file
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)  # Write the header
        for row in merged_rows:
            writer.writerow(row)

# Specify the input and output file paths
input_csv = 'contacts.csv'  # Replace with your input CSV file path
output_csv = 'output.csv'  # Replace with your desired output CSV file path

# Run the combination process
combine_csv(input_csv, output_csv)