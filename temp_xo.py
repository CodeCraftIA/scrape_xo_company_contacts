from tqdm import tqdm
import pandas as pd
import re
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


# Create empty lists to store data
names = []
addresses = []
emails = []
mobiles = []
telephones = []

options = uc.ChromeOptions()
driver = uc.Chrome(options=options)

url = "https://www.xo.gr/"

driver.get(url)

time.sleep(10)

def scrape(url):
    time.sleep(1)
    driver.get(url)
    time.sleep(4)
    # Define the JavaScript code to scroll the page
    scroll_script = """
        window.scrollBy(0, window.innerHeight);
    """

    # Scroll the page slowly with a delay of 0.5 seconds between each scroll
    for _ in range(3):
        driver.execute_script(scroll_script)
        time.sleep(0.5)

    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(4)

    # Define the list of CSS classes
    css_classes = ['li.span12.listing.paidListing.links_list', 'li.span12.listing.spListing.links_list', 'li.span12.listing.freeListing.links_list']

    # Initialize an empty list to store all found elements
    all_cards = []

    # Loop through each CSS class and find elements matching it
    for css_class in css_classes:
        cards = driver.find_elements(By.CSS_SELECTOR, css_class)
        all_cards.extend(cards)

    # Print the total number of cards found
    print("Found", len(all_cards), "cards")

    #span12 listing spListing links_list
    #"span12 listing freeListing links_list"
    #cards = driver.find_elements(By.CSS_SELECTOR, 'li.span12.listing.paidListing.links_list')
    #print("found ", len(cards), "cards")
    for card in all_cards:
        name=""
        address=""
        email=""
        mobile=""
        tele=""
        name_area = card.find_element(By.CLASS_NAME, 'listingBusinessNameArea')
        name = name_area.find_element(By.CLASS_NAME, 'et-v2').text.strip()
        try:
            address = card.find_element(By.CLASS_NAME, 'listingAddressInfo').text.strip()
        except Exception as e:
            address = ""

        try:
            email_cont = card.find_element(By.CLASS_NAME, 'listingSubMenu')
            # You may need to add a delay here to ensure the page loads completely
            email_element = email_cont.find_element(By.CSS_SELECTOR, 'a.et-v2-additional[href^="mailto:"]')
            email = email_element.get_attribute('href').replace('mailto:', '')
        except Exception as e:
            email = ""
        
        try:
            group = card.find_element(By.CLASS_NAME, 'btn-group')
            group_html = group.get_attribute('outerHTML')
            # Regular expression patterns
            phone1_pattern = re.compile(r'"phone1">(\d{3} \d{3} \d{4})<')
            mobile_phone_pattern = re.compile(r'"mobile.phone">(\d{3} \d{3} \d{4})<')

            # Find phone numbers using regex
            phone1_match = re.search(phone1_pattern, group_html)
            mobile_phone_match = re.search(mobile_phone_pattern, group_html)

            # Extract phone numbers
            tele = phone1_match.group(1) if phone1_match else None
            mobile = mobile_phone_match.group(1) if mobile_phone_match else None
        except Exception as e:
            tele=""
            mobile=""
        
        
        names.append(name)
        addresses.append(address)
        emails.append(email)
        mobiles.append(mobile)
        telephones.append(tele)
    

for page in tqdm(range(1,110)):
    try:
        url = "https://www.xo.gr/search/?what=τεχνικές+εταιρείες&page="+str(page)
        scrape(url)
    except Exception as e:
        print("Error on url: ", url)



driver.quit()

def write_excel(path):
    # Create DataFrame
    df = pd.DataFrame({
        'Company Name': names,
        'Phone': telephones,
        'Mobile': mobiles,
        'Email': emails,
        'Address': addresses,
    })
    # Write DataFrame to Excel
    with pd.ExcelWriter(path, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        print("Data scraped successfully and saved.")
        print("Processing complete. Check the generated files.")

def create_distinct_excel(input_path, output_path):
    # Read the existing Excel file
    df = pd.read_excel(input_path)
    
    # Drop duplicate rows
    df_distinct = df.drop_duplicates()
    
    # Write the distinct DataFrame to a new Excel file
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        df_distinct.to_excel(writer, index=False, sheet_name='Sheet1')
    
    print(f"Distinct data saved to {output_path}")

# Define the file names
input_file_name = 'xo10.xlsx'
output_file_name = 'xo_distinct10.xlsx'

# Create the original Excel file
write_excel(input_file_name)

# Create a new Excel file with distinct rows
create_distinct_excel(input_file_name, output_file_name)

