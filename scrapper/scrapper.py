# import logging
# from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# from random import seed
# from random import randint
# import re 
# import shutil
# import os
# from builtins import any as b_any
# from os import listdir
# from os.path import isfile, join


import time
import re
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from urllib.request import urlretrieve
import os

def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


def download_images(driver):
    # List all queries
    download = driver.find_elements(By.XPATH, "//div[@class='group relative flex bg-mirage px-4 py-6']")
    try:
        existent = pd.read_csv('/app/images/metadata.csv')
    except:
        existent = pd.DataFrame(columns=['name'
                        'query',
                        'time',
                        'blend',
                        'type',
                        'resolution',
                        'license',
                        'path'])
    metadatas = [existent]

    for im in download:
        url = im.find_element(By.CSS_SELECTOR, "img")
        metadata = {}
        if url not in existent['path']:
            url = url.get_attribute('src')
            metadata = im.text
            metadata = re.split(r"[\n\r]+", metadata)
            try:
                metadata = {'name':'Unamed', 
                        'query': metadata[0],
                        'time': metadata[1],
                        'blend': metadata[2],
                        'type': metadata[3],
                        'resolution': metadata[4],
                        'license': metadata[5]
                        }
            except:
                try:
                    metadata = {'name':'Unamed', 
                        'query': metadata[0],
                        'time': metadata[1],
                        'blend': metadata[2],
                        'type': 'unknown',
                        'resolution': 'unknown',
                        'license': metadata[3]
                        }
                except:
                    metadata = {'name':'Unamed', 
                        'query': metadata[0],
                        'time': metadata[1],
                        'blend': metadata[2],
                        'type': 'unknown',
                        'resolution': 'unknown',
                        'license':'unknown'
                        }

            metadata['path'] = url
            try:
                urlretrieve(url, '/app/images/' + metadata['query'] + '.png')
            except:
                urlretrieve(url, '/app/images/' + metadata['query'][0:30] + '.png')
                metadata['short_query'] =  metadata['query'][0:30] 
            metadatas.append(pd.DataFrame(metadata, index=[0]))

    metadatas = pd.concat(metadatas, ignore_index=False)
    metadatas.to_csv('/app/images/metadata.csv', index=False)

if __name__ == "__main__":

    chrome_options = set_chrome_options()
    driver = webdriver.Chrome(options=chrome_options)
    url = 'https://neuralblender.com/'
    driver.get(url)
    time.sleep(2)

    # Go to login page
    logging = driver.find_element(by=By.XPATH, value='/html/body/div/div[1]/header/div[2]/nav/div/button').click()
    time.sleep(2)

    # Login
    username = driver.find_element(by=By.XPATH, value='/html/body/div/div[2]/div/div/div/div[1]/div[2]/form/div/div[1]/div[1]/input')
    username.send_keys(os.getenv('EMAIL'))
    password = driver.find_element(by=By.XPATH, value='/html/body/div/div[2]/div/div/div/div[1]/div[2]/form/div/div[1]/div[2]/div[1]/input')
    username.send_keys(os.getenv('PASS'))
    login = driver.find_element(By.XPATH, value='/html/body/div/div[2]/div/div/div/div[1]/div[2]/form/div/div[2]/button').click()
    time.sleep(2)    
    art_page = driver.get('https://neuralblender.com/my-art')
    time.sleep(2)
    download_images(driver)

    driver.close()