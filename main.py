import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

GOOGLE_FORM_LINK = ('https://docs.google.com/forms/d/e/1FAIpQLSdX6aftpsyzbtKyxotpUmIVkSaz8n2JBsf0oIEppMZ0Pp1zXQ'
                    '/viewform?usp=pp_url')
RENTAL_LIST_LINK = 'https://www.apartments.com/chicago-il/'


# FUNCTION TO IMPORT INFORMATION ABOUT PROPERTY TO GOOGLE FORM
def import_property(address, price, link):
    # OPTIONS FOR GOOGLE CHROME
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=options)
    driver.get(GOOGLE_FORM_LINK)
    time.sleep(2)
    # INPUT ADDRESS TO GOOGLE FORM
    input_address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div['
                                                  '2]/div/div[1]/div/div[1]/input')
    input_address.send_keys(address)
    # INPUT PRICE/MONTH TO GOOGLE FORM
    input_price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]'
                                                '/div/div[1]/div[2]/textarea')
    input_price.send_keys(price)
    # INPUT LINK TO GOOGLE FORM
    input_link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]'
                                               '/div/div[1]/div[2]/textarea')
    input_link.send_keys(link)
    # SEND TO GOOGLE FORM
    send_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    send_button.click()
    driver.quit()


# ACCESS TO WEBSITE
headers = {
    'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}
response = requests.get(RENTAL_LIST_LINK, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

# TAKE DATA FROM WEBSITE TO LIST
price_data = soup.find_all("p", class_="property-pricing")
address_data = soup.find_all("div", class_="property-address js-url")
link_data = soup.find_all("a", class_="property-link")

new_link = [link_data[n]['href'] for n in range(len(link_data)) if link_data[n]['href'] != link_data[n-1]['href']]

# PUSH DATA TO GOOGLE FORM
for n in range(len(price_data)):
    price = price_data[n].get_text()
    address = address_data[n].get_text()
    link = new_link[n]
    import_property(address, price, link)