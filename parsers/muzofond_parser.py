from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from urllib import request
import os

compositor_name = input('Input author name like in muzofond.fm site: ').strip().lower()

os.makedirs('music', exist_ok=True)


song_count = 0

options = FirefoxOptions()
options.headless = True
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=Service(GeckoDriverManager().install()), options=options)

page = 1
while True:
    driver.get(f'https://muzofond.fm/collections/artists/{compositor_name}/{page}')  # Fix me: При странице, которой нет - редирект на 1 идет
    elements = driver.find_elements(By.CLASS_NAME, 'item')

    count_on_page = 0
    for el in elements:
        try:
            name = el.find_element(By.TAG_NAME, 'h3').text.strip()
        except NoSuchElementException:
            continue
        if compositor_name not in name.lower(): continue
        song_count += 1
        count_on_page += 1
        try:
            print(name)
            url = el.find_element(By.CLASS_NAME, 'play').get_attribute('data-url')
            
            request.urlretrieve(url, 'music/' + name + '.mp3')
        except:
            print('error: ' + name)
            song_count -= 1
    if count_on_page == 0: break
    print(f'Parsing from {page} finished! Parsed {count_on_page} songs.')
    page += 1

driver.close()

print('Total songs:', song_count)
