from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
import numpy as np
import requests # Used to make HTTP requests to the API
import json # Used to process JSON strings
import urllib.request, json
import os
import glob

# Function to interact with dropdown
def interact_with_dropdown(driver, container_id, value_to_select, wait):
    # Locate the dropdown container by its ID
    dropdown_container = driver.find_element(By.ID, container_id)

    # Click on the input field to open the dropdown
    input_field = driver.find_element(By.ID, container_id)
    input_field.click()

    # Explicitly wait for the dropdown options to appear
    wait.until(EC.visibility_of_element_located((By.ID, container_id)))

    # Use the Select class to interact with the dropdown
    dropdown_select = Select(driver.find_element(By.ID, f'{container_id}_ddValue'))

    # Select the value
    dropdown_select.select_by_value(value_to_select)

def rename_file(current_file_name, new_file_name):
    # Use the os.rename() function to rename the file
    try:
        os.rename(current_file_name, new_file_name)
        print(f"File '{current_file_name}' renamed to '{new_file_name}'")
    except FileNotFoundError:
        print(f"File '{current_file_name}' not found.")
    except FileExistsError:
        print(f"File '{new_file_name}' already exists.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def extract_single_park_visit_data(park_code):
    # Initialize a web driver (you can use other drivers like Firefox or Edge)
    driver = webdriver.Chrome()

    # Navigate to the URL with the iframe
    url = 'https://irma.nps.gov/Stats/SSRSReports/Park%20Specific%20Reports/Monthly%20Public%20Use?Park=WHSA'
    driver.get(url)

    # Wait for the iframe to load
    wait = WebDriverWait(driver, 10)
    iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))

    # Switch to the iframe
    driver.switch_to.frame(iframe)
    
    # Interact with the first dropdown
    interact_with_dropdown(driver, 'ReportViewer_ctl04_ctl03', str(park_code), wait)

    time.sleep(2) 

    for i in range(1,120):
        check_file_exist_path = "/Users/leo/Downloads/{}_{}_monthly_visit.csv".format(park_code,i)
        if os.path.exists(check_file_exist_path):
            continue
        # Interact with the second dropdown
        interact_with_dropdown(driver, 'ReportViewer_ctl04_ctl05', str(i), wait)
        time.sleep(3)

        # Continue with other interactions as needed, if any
        view_report_click = driver.find_element(By.ID, 'ReportViewer_ctl04_ctl00')
        view_report_click.click()
        time.sleep(3)

        dropdown_container = driver.find_element(By.ID, 'ReportViewer_ctl05_ctl04_ctl00_Button')
        
        time.sleep(3)
        # Click on the input field to open the dropdown
        input_field = driver.find_element(By.ID, 'ReportViewer_ctl05_ctl04_ctl00_Button')
        input_field.click()

        time.sleep(3)
        # Explicitly wait for the dropdown options to appear
        wait.until(EC.visibility_of_element_located((By.ID, 'ReportViewer_ctl05_ctl04_ctl00_Button')))

        time.sleep(3)
        # Export as csv
        csv_option = driver.find_element(By.XPATH, "//a[contains(text(), 'CSV (comma delimited)')]")
        time.sleep(3)
        csv_option.click()
        
        time.sleep(5)
        try:
            matching_files = glob.glob(f"/Users/leo/Downloads/Monthly Public*")
            old_file_name = matching_files[0]
            new_file_name = "/Users/leo/Downloads/{}_{}_monthly_visit.csv".format(park_code,i)
            rename_file(old_file_name, new_file_name)
        except:
            continue

        # Close the web driver when you're done
        time.sleep(5) 
    driver.quit()


if __name__ == "__main__":
    park_to_option_value = json.load(open("NPS_park_to_option_value.json","r"))
    park_info = json.load(open("national_park_code.json","r"))

    for key in park_info:
        print(key.strip())
        park_code = park_to_option_value[key.strip()]
        extract_single_park_visit_data(park_code)
    








