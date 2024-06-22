from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
import csv
import os
import re
import time

class ContactScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.organization_domain = organization_domain
        self.visited_departments = set()
        self.processed_names = set()
        self.processed_phone_numbers = set()
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

        if not os.path.exists('contacts.csv'):
            with open('contacts.csv', 'w', newline='') as csvfile:
                fieldnames = ['Name', 'Phone Number', 'Email', 'Profile URL', 'Email Pattern']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

        for filename in ['names.txt', 'phone_numbers.txt', 'emails.txt', 'departments.txt']:
            if not os.path.exists(filename):
                open(filename, 'w').close()

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

                with open('departments.txt', 'a') as dept_file:
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

                                if name not in self.processed_names:
                                    print(f"Found Name: {name}")
                                    self.processed_names.add(name)

                                    with open('names.txt', 'a') as name_file:
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
                    for row in rows:
                        try:
                            th = row.find_element(By.TAG_NAME, 'th')
                            td = row.find_element(By.TAG_NAME, 'td')
                            if th and td:
                                if 'Phone' in th.text:
                                    phone_number = self.extract_phone_number(td)
                                    if phone_number and phone_number not in self.processed_phone_numbers:
                                        print(f"Phone number found: {phone_number}")
                                        self.processed_phone_numbers.add(phone_number)

                                        with open('phone_numbers.txt', 'a') as phone_file:
                                            phone_file.write(phone_number + '\n')

                                        self.write_to_csv(name, phone_number, profile_url, '-')
                                        phone_number_found = True
                                elif 'E‑mail' in th.text:
                                    email_address = self.extract_email_address(td)
                                    if email_address:
                                        matched_pattern = self.match_email_pattern(email_address, name)
                                        self.write_to_csv(name, '-', profile_url, matched_pattern)
                        except StaleElementReferenceException:
                            print("Stale element reference, retrying row interaction...")
                            retry_attempts -= 1
                            time.sleep(2)
                            break  # Break and retry the outer loop to re-fetch rows
                    else:
                        break  # If no exception occurred, exit the retry loop

                    if not phone_number_found:
                        print(f"No phone number found for {name}. Recording '-'")
                        self.write_to_csv(name, '-', profile_url, '-')
                        with open('phone_numbers.txt', 'a') as phone_file:
                            phone_file.write('-' + '\n')
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
            return None

    def extract_email_address(self, td):
        try:
            a_tag_mailto = td.find_element(By.CSS_SELECTOR, 'a[href^="mailto:"]')
            email_address = a_tag_mailto.get_attribute('href').split('mailto:')[-1]
            print(f"Email address found: {email_address}")
            with open('emails.txt', 'a') as email_file:
                email_file.write(email_address + '\n')
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

    def write_to_csv(self, name, phone_number, profile_url, email_pattern):
        with open('contacts.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name, phone_number, profile_url, email_pattern])

    def close(self):
        self.driver.quit()

# usage:
organization_domain = input("Please enter the organization domain: ")
base_website_url = input("Please enter the base website URL: ")
scraper = ContactScraper(base_website_url)
scraper.visit_website()
scraper.close()
