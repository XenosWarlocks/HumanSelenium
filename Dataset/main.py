import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
from collections import defaultdict

class ContactScraper:
    def __init__(self, base_url, organization_domain):
        self.base_url = base_url
        self.organization_domain = organization_domain
        self.visited_departments = set()
        self.processed_entries = set()  # To track processed entries
        self.email_patterns = [
            r"{last}@",
            r"{first}\.{last}@"
        ]

        options = Options()
        options.headless = True
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Set up the output directory
        self.output_dir = 'gen_files'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.csv_filename = os.path.join(self.output_dir, 'contacts.csv')
        self.init_csv()

    def init_csv(self):
        # Initialize CSV file with headers if it doesn't exist
        if not os.path.exists(self.csv_filename):
            with open(self.csv_filename, 'w', newline='') as csvfile:
                fieldnames = ['Name', 'Phone Number', 'Email', 'Profile URL', 'Email Pattern']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

    def visit_website(self):
        try:
            self.driver.get(self.base_url)
            wait = WebDriverWait(self.driver, 10)
            li_tags = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.crossroad-links__item')))
            department_urls = []

            for li in li_tags:
                try:
                    a_tag = li.find_element(By.TAG_NAME, 'a')
                    href = a_tag.get_attribute('href')
                    if href:
                        department_urls.append(href)
                except NoSuchElementException:
                    print(f"No <a> tag found in <li> element: {li}")

            for department_url in department_urls:
                self.visit_department_url(department_url)

            # After visiting all departments, navigate back to the base URL
            self.driver.get(self.base_url)

        except Exception as e:
            print(f"An error occurred: {e}")

    def visit_department_url(self, department_url):
        try:
            self.driver.get(department_url)
            wait = WebDriverWait(self.driver, 10)
            department_name = department_url.split('/')[-1]
            if department_url not in self.visited_departments:
                print(f"Visiting Department URL: {department_url}")
                self.visited_departments.add(department_url)

                dept_file_path = os.path.join(self.output_dir, 'departments.txt')
                with open(dept_file_path, 'a') as dept_file:
                    dept_file.write(f"{department_name} - {department_url}\n")

                li_tags = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.crossroad-links__item')))
                names_to_process = []

                for li in li_tags:
                    try:
                        a_tag = li.find_element(By.TAG_NAME, 'a')
                        href = a_tag.get_attribute('href')
                        if href:
                            parts = href.split('-')
                            if len(parts) >= 2:
                                last_two_parts = [part.capitalize() for part in parts[-2:]]
                                name = ' '.join(last_two_parts)

                                if name not in self.processed_entries:
                                    print(f"Found Name: {name}")
                                    self.processed_entries.add(name)

                                    names_file_path = os.path.join(self.output_dir, 'names.txt')
                                    with open(names_file_path, 'a') as name_file:
                                        name_file.write(name + '\n')

                                    full_url = urljoin(department_url, href)
                                    names_to_process.append((full_url, name))

                    except NoSuchElementException:
                        print(f"No <a> tag found in <li> element: {li}")

                for full_url, name in names_to_process:
                    self.visit_profile_url(full_url, name)

                # After processing all names, navigate back to department URL
                self.driver.get(department_url)

        except Exception as e:
            print(f"An error occurred while visiting the department URL: {e}")

    def visit_profile_url(self, profile_url, name):
        try:
            self.driver.get(profile_url)
            print(f"Visiting Profile URL: {profile_url}")
            wait = WebDriverWait(self.driver, 10)

            retry_attempts = 3  # Retry mechanism for handling stale elements
            while retry_attempts > 0:
                try:
                    table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'table-vcard')))
                    rows = table.find_elements(By.TAG_NAME, 'tr')

                    phone_number_found = False
                    email_found = False
                    for row in rows:
                        try:
                            th = row.find_element(By.TAG_NAME, 'th')
                            td = row.find_element(By.TAG_NAME, 'td')
                            if th and td:
                                if 'Phone' in th.text:
                                    phone_number = self.extract_phone_number(td)
                                    if phone_number and phone_number != '-':
                                        print(f"Phone number found: {phone_number}")
                                        self.processed_entries.add((name, phone_number, '-', profile_url, '-'))

                                        phone_file_path = os.path.join(self.output_dir, 'phone_numbers.txt')
                                        with open(phone_file_path, 'a') as phone_file:
                                            phone_file.write(phone_number + '\n')

                                        self.write_to_csv(name, phone_number, '-', profile_url, '-')
                                        phone_number_found = True
                                    else:
                                        print(f"No phone number found for {name}. Recording '-'")
                                        self.write_to_csv(name, '-', '-', profile_url, '-')
                                        phone_file_path = os.path.join(self.output_dir, 'phone_numbers.txt')
                                        with open(phone_file_path, 'a') as phone_file:
                                            phone_file.write('-\n')

                                elif 'E‑mail' in th.text:
                                    email_address = self.extract_email_address(td)
                                    if email_address and (name, '-', email_address, profile_url, '-') not in self.processed_entries:
                                        print(f"Email address found: {email_address}")
                                        self.processed_entries.add((name, '-', email_address, profile_url, '-'))

                                        email_file_path = os.path.join(self.output_dir, 'emails.txt')
                                        with open(email_file_path, 'a') as email_file:
                                            email_file.write(email_address + '\n')

                                        matched_pattern = self.match_email_pattern(email_address, name)
                                        self.write_to_csv(name, '-', email_address, profile_url, matched_pattern)
                                        email_found = True
                        except StaleElementReferenceException:
                            print("Stale element reference, retrying row interaction...")
                            retry_attempts -= 1
                            time.sleep(2)
                            break  # Break and retry the outer loop to re-fetch rows
                    else:
                        break  # If no exception occurred, exit the retry loop

                    if not email_found:
                        print(f"No email found for {name}. Recording '-'")
                        self.write_to_csv(name, '-', '-', profile_url, '-')
                        email_file_path = os.path.join(self.output_dir, 'emails.txt')
                        with open(email_file_path, 'a') as email_file:
                            email_file.write('-\n')

                except StaleElementReferenceException:
                    print("Stale element reference, retrying profile interaction...")
                    retry_attempts -= 1
                    time.sleep(2)

        except Exception as e:
            print(f"An error occurred while visiting the profile URL: {e}")

    def extract_phone_number(self, td):
        try:
            a_tag_tel = td.find_element(By.CSS_SELECTOR, 'a[href^="tel:"]')
            phone_number = a_tag_tel.get_attribute('href').split('tel:')[-1]
            return phone_number
        except NoSuchElementException:
            return '-'

    def extract_email_address(self, td):
        try:
            a_tag_mailto = td.find_element(By.CSS_SELECTOR, 'a[href^="mailto:"]')
            email_address = a_tag_mailto.get_attribute('href').split('mailto:')[-1]
            return email_address
        except NoSuchElementException:
            return None

    def match_email_pattern(self, email_address, name):
        first, last = name.split()
        patterns = {
            f"{last}@{self.organization_domain}": "{last}@",
            f"{first}.{last}@{self.organization_domain}": "{first}.{last}@"
        }
        for pattern, placeholder in patterns.items():
            if email_address.lower().startswith(pattern.lower()):
                print(f"Email matches pattern: {placeholder}")
                return placeholder
        print(f"No specific pattern matched for email: {email_address}")
        return "Unknown Pattern"

    def write_to_csv(self, name, phone_number, email_address, profile_url, email_pattern):
        entry_key = (name, '-', '-', profile_url, '-')
        
        # Check if the entry already exists to avoid duplicates
        with open(self.csv_filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            found = False
            
            for row in rows:
                if tuple(row[:4]) == entry_key:
                    row[2] = email_address  # Update email_address
                    row[4] = email_pattern  # Update email_pattern
                    found = True
                    break
            
            if not found:
                rows.append([name, phone_number, email_address, profile_url, email_pattern])

        # Rewrite the CSV file with updated or new data
        with open(self.csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)

        # Check if the entry is already processed to avoid duplicates
        entry_key = (name, phone_number, email_address, profile_url, email_pattern)
        if entry_key not in self.processed_entries:
            self.processed_entries.add(entry_key)

        # Write to phone_numbers.txt if phone_number is valid
        if phone_number and phone_number != '-':
            phone_file_path = os.path.join(self.output_dir, 'phone_numbers.txt')
            with open(phone_file_path, 'a') as phone_file:
                phone_file.write(phone_number + '\n')

    def close(self):
        self.driver.quit()

# usage:
if __name__ == "__main__":
    organization_domain = input("Please enter the organization domain: ")
    base_website_url = input("Please enter the base website URL: ")
    
    scraper = ContactScraper(base_website_url, organization_domain)
    scraper.visit_website()
    scraper.close()

