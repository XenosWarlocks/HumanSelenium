from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import csv
import os
import re

class ContactScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_departments = set()      # Track visited departments to avoid duplicates
        self.processed_names = set()          # Track processed names to avoid duplicates
        self.processed_phone_numbers = set()  # Track processed phone numbers to avoid duplicates
        self.email_patterns = [
            r"{last}@",                      
            r"{first}\.{last}@"              
        ]
        self.organization_domain = "law.muni.cz"  # Replace with the actual domain

        # Setup the Selenium webDriver in headless
        options - Options()
        options.headless = True
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # set the path to your ChromeDriver executable if not in the system PATH
        self.driver = webdriver.Chrome(options=options)

        # Initialize the csv file and write the headers if the file doesn't exist
        if not os.path.exists('contacts.csv'):
            with open('contacts.csv', 'w', newline='') as csvfile:
                fieldnames = ['Name', 'Phone Number', 'Profile URL', 'Email Pattern']
                writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
                writer = writeheader()

        # Ensure that the text files exist, create them if they don't
        for filename in ['names.txt', 'phone_numbers.txt', 'emails.txt', 'departments.txt']
        if not os.path.exists(filename):
            open(filename, 'w').close()


    def visit_website(self):
        try:
            self.drive.get(self.base_url)
            wait = WebDriverWait(self.driver, 10)
            li_tags = wait.until(EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, 'li.crossroad-links__item'
            )))
            for li in li_tags:
                try:
                    a_tag = li.find_element(By.TAG_NAME, 'a')
                    href = a_tag.get_attribute('href')
                    if href:
                        self.visit_department_url(href)
                except NoSuchElementException:
                    print(f"An error occurred: {e}")
                    
        except Exception as e:
            print(f"An error occurred: {e}")


    def visit_department_url(self, department_url):
        try:
            self.driver.get(department_url)
            wait = WebDriverWait(self.driver, 10)
            department_name = department_url.splite('/')[-1]
            if department_url not in self.visited_deparments:
                print(f"Visiting Department URL: {department_url}")
                self.depaertment_visited.add(department_url)

                # Write the department name and URL to the departments.txt file
                with open('departments.txt', 'a') as dept_file:
                    dept_file.write(f"{department_name} - {department_url}\n")

                li_tags = wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'li.crossroad-links__item')
                ))
                for li in li_tags:
                    try:
                        a_tag = li.find_element(By.TAG_NAME, 'a')
                        href = a_tag.get_attribute('href')
                        if href:
                            parts = href.split('-')
                            if len(parts) >= 2:
                                last_two_parts = [parts.capitalized() for part in parts[-2:]]
                                name = ' '.join(last_two_parts)

                                if name not in self.processed_names:
                                    print(f"Found Name: {name}")
                                    self.processed_names.add(name)

                                    # Write the name to the names.txt file
                                    with open('namse.txt', 'a') as name_file:
                                        name_file.write(name + '\n')
                                    full_url = urljoin(department_url, href)
                                    self.visit_profile_url(full_url, name)
                    except NoSuchElementException:
                        print(f"No <a> tag found in <li> element: {li}")
        except Exception as e:
            print(f"An error occurred while visiting the department URL: {e}")

    def visit_profile_url(self, profile_url, name):
        try:
            self.driver.get(profile_url)
            print(f"Visiting Profile URL: {profile_url}")
            wait = WebDriverWait(self.driver, 10)
        except Exception as e:
            print(f"An error occurred while visiting the profile URL: {e}")
            
