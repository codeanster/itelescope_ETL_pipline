from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import warnings
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import time
from nltk.corpus import stopwords
nltk_stopwords = set(stopwords.words('english'))
from astropy.coordinates import SkyCoord
import itertools
import datefinder
from csv import writer
        
warnings.filterwarnings("ignore", category=DeprecationWarning) 
load_dotenv()
chromedriver = "chromedriver.exe"
driver = webdriver.Chrome(chromedriver)
chrome_options = Options()

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)
        
#get it to work on cloud
# chrome_options.add_argument("--headless")
#link to sign into itelescope
link = 'https://go.itelescope.net/?_gl=1*1nsajcx*_ga*MTA1NTMyNDcxNS4xNjQ1NDk5ODUw*_ga_1PW2XEZ2KC*MTY0NTQ5OTg0OC4xLjAuMTY0NTQ5OTg0OC4w'

driver.get(link)
time.sleep(3)

#login
user_name_box = driver.find_element_by_name('UsernameTextBox').send_keys(os.getenv('USER'))
password_box = driver.find_element_by_xpath("//input[@id='PasswordTextBox']").send_keys(os.getenv('USERPASS'))
login_button = driver.find_element_by_name('LoginButton').click()

time.sleep(2)

#save info for download
download_pw = driver.find_element_by_class_name('enable-select').text
download_link = 'https://www.itelescope.net/premium-images'
driver.get(download_link)

time.sleep(2)
#while on download page, let's get the date and the name of the object
info_string = driver.find_element_by_id('block-yui_3_17_2_1_1656355145026_122873').text

matches = datefinder.find_dates(info_string[:20])

match = next(matches)
date = match.date()
print(date)
#let's get the name of the object and confirm that it exists
text_without_stopword = [word for word in info_string[20:70].split() if word.lower() not in nltk_stopwords]

#try every 2 pair combination until we find something in... astropy
pair_order_list = itertools.combinations(text_without_stopword,2)
 
for pair in pair_order_list:
    try:
        target_coord = SkyCoord.from_name(pair[0] + pair[1])
        name = f'{pair[0]}_{pair[1]}'
        print(f'Object Name confirmed: {name}.')
        break
    except:
        pass

#download latest 20 plan
dl20 = driver.find_elements_by_class_name('sqs-button-element--primary')[0].click()

#enter download_pw from previous page
password_box = driver.find_element_by_class_name('dig-TextInput-input').send_keys(download_pw)

time.sleep(3)

#click buttons to start download
driver.find_element_by_class_name('require-password-view__button-container').click()

time.sleep(3)
driver.find_element_by_class_name('mc-button-content').click()

print('downloading...')
time.sleep(180) #this is for less than 1GB, adjust when needed


#save record of download date        
row_contents = [date,name]
append_list_as_row('meta.csv',row_contents)  
print('Saving to csv...')
 
driver.quit()