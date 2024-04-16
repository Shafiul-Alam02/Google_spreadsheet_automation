import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

username = "username"
password = "password"

# Select the account from the dropdown menu
account_option_value = "account"  # Value of the option you want to select
start_date_value = "09-04-2024"
end_date_value = "09-04-2024"



# Find the path of the Chrome executable
chrome_path = None

# Check common installation paths for Chrome on Windows
chrome_paths = [
    os.path.join(os.getenv("PROGRAMFILES(X86)"), "Google", "Chrome", "Application", "chrome.exe"),
    os.path.join(os.getenv("PROGRAMFILES"), "Google", "Chrome", "Application", "chrome.exe"),
]

for path in chrome_paths:
    if os.path.exists(path):
        chrome_path = path
        break

if chrome_path is None:
    raise FileNotFoundError("Chrome is not installed in the default locations.")

# Initialize Chrome WebDriver with the Chrome executable path
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = chrome_path
driver = webdriver.Chrome(options=chrome_options)

# Open web
driver.get('https://ibank.thecitybank.com/login.php')




# Wait for username field to be visible
username_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'userID')))
username_field.send_keys(username)

# Wait for password field to be visible
password_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'password')))
password_field.send_keys(password)

# Submit the form
password_field.submit()

pyautogui.press('enter')

# Add a sleep to wait for the login process to complete (optional)
time.sleep(1)


# Wait for the "Account Details" link to be visible and clickable
account_details_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Account Details")]')))

# Click the "Account Details" link
account_details_link.click()


#################################################

# # Find the dropdown element and select the desired option
account_dropdown = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'cboAccount')))
account_dropdown.send_keys(account_option_value)

# Find the start date and end date fields and input manual values
start_date_field = driver.find_element(By.ID, 'txtStart')
start_date_field.clear()
start_date_field.send_keys(start_date_value)

end_date_field = driver.find_element(By.ID, 'txtEnd')
end_date_field.clear()
end_date_field.send_keys(end_date_value)

# Submit the form (assuming clicking the search button)
search_button = driver.find_element(By.ID, 'searchSubmit')
search_button.click()

time.sleep(1)
##########################################################


# Get the HTML content from the current webpage
html_content = driver.page_source

# Close the WebDriver since we have captured the HTML content
driver.quit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table using its specific attributes
table = soup.find('table', {'width': '680', 'border': '0', 'cellpadding': '1', 'cellspacing': '1', 'bgcolor': '#F4F4F4'})


# Extract data from the table
data_rows = table.find_all('tr')  # Assuming data is in table rows

# Extracting data into a list of lists
data_list = []
for row in data_rows:
    cells = row.find_all('td')
    row_data = [cell.text.strip() for cell in cells]
    data_list.append(row_data)

#Define the scope and credentials to access Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

# Authorize with Google Sheets
client = gspread.authorize(creds)

# Open the Google Sheet by its ID
sheet_id = 'Sheetid'
spreadsheet = client.open_by_key(sheet_id).sheet1  # Assume you are working with the first sheet


# Clear existing data in the Google Sheet (optional)
spreadsheet.clear()


# Define the range where you want to dump the data (e.g., starting from cell A1)
start_cell = 'A1'

# Dump the data list into the spreadsheet
spreadsheet.update(start_cell, data_list)

# print(data_list)
print("Data uploaded to Google Sheets.")