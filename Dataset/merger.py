############################################################################
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename


def main():
    # Hide the root Tkinter window
    Tk().withdraw()


    # Ask the user to upload the main Excel file
    print("Please select the main Excel file:")
    main_file_path = askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if not main_file_path:
        print("No file selected. Exiting.")
        return


    # Ask the user to upload the verified Excel file
    print("Please select the verified Excel file:")
    verified_file_path = askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if not verified_file_path:
        print("No file selected. Exiting.")
        return


    # Load the main and verified Excel files
    try:
        main_df = pd.read_excel(main_file_path)
        verified_df = pd.read_excel(verified_file_path)
    except Exception as e:
        print(f"Error loading Excel files: {e}")
        return


    # Ensure the required columns exist
    if 'Email Address' not in main_df.columns:
        print("Main file does not contain 'Email Address' column.")
        return


    if 'Email' not in verified_df.columns or 'Email Status' not in verified_df.columns:
        print("Verified file must contain 'Email' and 'Email Status' columns.")
        return


    # Merge the main DataFrame with the verified DataFrame on email addresses
    merged_df = main_df.merge(verified_df, left_on='Email Address', right_on='Email', how='left')


    # Filter out rows where Email Status is 'unknown'
    filtered_df = merged_df[merged_df['Email Status'] != 'unknown']


    # Drop the columns from the merged DataFrame that are no longer needed
    filtered_df = filtered_df.drop(columns=['Email', 'Email Status'])


    # Ask the user to specify the output file path
    print("Please select the location to save the updated Excel file:")
    output_file_path = asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if not output_file_path:
        print("No file selected. Exiting.")
        return


    # Save the filtered DataFrame to the output file
    try:
        filtered_df.to_excel(output_file_path, index=False)
        print(f"Filtered file saved successfully to {output_file_path}.")
    except Exception as e:
        print(f"Error saving the filtered file: {e}")


if __name__ == "__main__":
    main()



