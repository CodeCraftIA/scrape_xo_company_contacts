# scrape_xo_company_contacts
This script scrapes technical company information from the website xo.gr, extracting details such as company names, addresses, emails, phone numbers, and mobile numbers. The data is saved into an Excel file, and a second file with duplicate entries removed is also generated.  Features

# Description
This script scrapes technical company information from the website xo.gr, extracting details such as company names, addresses, emails, phone numbers, and mobile numbers. The collected data is saved into an Excel file and then a second Excel file is generated with duplicate entries removed. The script uses Selenium with an undetected Chrome driver to handle dynamic content loading.

# Features
Scrapes company names, addresses, emails, phone numbers, and mobile numbers from xo.gr.
Handles dynamic content loading using Selenium with undetected Chrome driver.
Saves scraped data into an Excel file.
Generates a second Excel file with duplicate entries removed.

# Requirements
Python

# Required Python packages:
pandas
re
time
undetected-chromedriver
tqdm
selenium
