# HumanSelenium

![HumanSelenium Logo](https://raw.githubusercontent.com/XenosWarlocks/HumanSelenium/main/images/Logo.webp)
This project aims to develop a tool using Selenium WebDriver to automate data scraping tasks from websites, mimicking human interaction.  Think of it as an extension of your arm in the digital world, collecting data just like you would.


This Python script utilizes Selenium to scrape contact information from a website, including names, phone numbers, and emails. It writes the data to CSV files and logs processed entries to avoid duplicates.

## Prerequisites

- Python 3.x installed on your system.
- Google Chrome browser.
- `pip` package manager.
- Reliable internet connection.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/XenosWarlocks/HumanSelenium.git
   cd HumanSelenium
   ```

## Usage
1. Run the script:
   - Navigate to the directory where the code is located. (inside the dataset folder)
   - Execute the script: `python main.py`
2. Input required information:
   - Enter the base website URL when prompted. Example: `https://www.example.com`
   - Enter the organization's domain name when prompted. `Example: example.com`
3. Process:
   - The script will launch a headless Chrome browser.
   - It will navigate through the website, scrape contact details, and write them to CSV files (`contacts.csv`, `phone_numbers.txt`, `emails.txt`, `departments.txt`).
4. Error Handling:
   - The script includes error handling for various exceptions (e.g., `NoSuchElementException`, `StaleElementReferenceException`) to ensure robustness.

## Project Update - Handling Duplicate Data and New Feature
1. New Issue: Duplicate Data
   - I encountered an issue where duplicate entries were causing inconsistencies in our output files. This was particularly challenging when processing large datasets, such as CSV files containing contact information.
2. Solution Implemented
   - To overcome this issue, I enhanced our script to check for existing entries before writing to the output file. By leveraging Python's `defaultdict` from the `collections` module, I efficiently managed and combined rows based on unique identifiers, ensuring that each entry is processed only once. This improvement ensures data integrity and reduces redundancy in the output.
3. New Feature Implemented
   - In addition to addressing duplicate data, I have introduced a new feature that allows seamless integration with the `gen_files` folder. All generated files, including the input CSV (`contacts.csv`) and the output CSV (`output.csv`), are now managed within the `gen_files`. Additionally, the script reads input files directly from the `gen_files` directory and writes the output CSV file (`output.csv`) within the same folder. This streamlined approach enhances usability and maintains organization within the project structure.

## Advanced Options
- Customization: Modify CSS selectors (`By.CSS_SELECTOR`) within the script to match the HTML structure of the target website.
- Logging: Detailed logging of visited URLs and processed entries to `departments.txt` and other log files.
- Duplicate Prevention: Entries are logged in `processed_entries` set to prevent duplicate data in CSV output.

## Legal and Ethical Considerations
Ensure compliance with the target website's terms of service and legal requirements before scraping.
Respect robots.txt guidelines and use appropriate scraping intervals to avoid overloading the website.

## Contributing
Contributions are welcome! If you encounter bugs or have suggestions for improvements, please [open an issue](https://github.com/XenosWarlocks/HumanSelenium/issues/new) or fork the repository and submit a pull request.
   
