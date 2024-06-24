### Contact Scraper

This Contact Scraper script (`main.py`) is designed to extract contact information from a specified organization's website and store it in various formats like CSV, JSON, or Excel. It utilizes Selenium for web scraping and handles different elements such as names, phone numbers, and email addresses.

## Features
- Web Scraping: Uses Selenium to navigate through departmental pages and profile pages to extract contact details.
- Output Formats: Supports exporting data to CSV, JSON, and Excel formats based on user input.
- Data Handling: Prevents duplicates and combines data intelligently for each individual based on their contact information.
- User Interaction: Prompts users to enter organization domain, base website URL, and desired output format.
- Error Handling: Catches and reports errors during the scraping process to ensure robust operation.

## Requirements
Python 3.6+
Selenium
ChromeDriver (automatically managed by `webdriver_manager`)
OpenPyXL (for Excel file handling)
pandas (for Excel file handling)

### Data Combiner

The Data Combiner script (`combiner.py`) reads contact information from CSV, JSON, or Excel files and combines rows for each individual to create consolidated output files. It handles different data formats and ensures seamless integration of contact details.

## Notes
- Make sure to have the input file (`contacts.csv`, `contacts.json`, or `contacts.xlsx`) in the specified format available in the gen_files directory.
- Adjust the output folder (`gen_files`) as per your requirement to store the generated combined files.
- Check the console output for confirmation and any error messages during script execution.
