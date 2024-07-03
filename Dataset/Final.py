import pandas as pd
import os


# Define paths
input_file = 'gen_files/output.csv'
output_file = 'C:/***/your_path/output/final.csv'
removed_file = 'C:/***/your_path/output/removed.csv'


# Read the input CSV
df = pd.read_csv(input_file)


# Function to check if an email is of the form 'numbers@'
def is_numeric_and_at(email):
    parts = email.split('@')
    if len(parts) != 2:
        return False  # Email should have exactly one '@'
    numeric_part = parts[0]
    if numeric_part.isdigit():
        return True  # Numeric part should consist only of digits
    return False


# Create a mask for rows to be removed
mask = df['Email'].astype(str).apply(is_numeric_and_at)


# Filter out rows to be removed and save to removed.csv
removed_df = df[mask]
removed_df.to_csv(removed_file, index=False)
print(f"Removed data saved to {removed_file}")


# Filter out rows where email is 'numbers@'
df = df[~mask]


# Save the filtered data to final.csv
df.to_csv(output_file, index=False)
print(f"Filtered data saved to {output_file}")


