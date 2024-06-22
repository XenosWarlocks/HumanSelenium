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

## Advanced Options
- Customization: Modify CSS selectors (`By.CSS_SELECTOR`) within the script to match the HTML structure of the target website.
- Logging: Detailed logging of visited URLs and processed entries to `departments.txt` and other log files.
- Duplicate Prevention: Entries are logged in `processed_entries` set to prevent duplicate data in CSV output.

## Legal and Ethical Considerations
Ensure compliance with the target website's terms of service and legal requirements before scraping.
Respect robots.txt guidelines and use appropriate scraping intervals to avoid overloading the website.

## Contributing
Contributions are welcome! If you encounter bugs or have suggestions for improvements, please [open an issue](https://github.com/XenosWarlocks/HumanSelenium/issues/new) or fork the repository and submit a pull request.
   
