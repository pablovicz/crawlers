from utils import click_nav_btn, collect_table_data
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import re
import pandas as pd
import os


def collect_cnpj(content):
    pattern = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
    match = re.search(pattern, content)
    if match:
        return match.group()
    return None


def collect_phone(content):
    pattern = r'Telefone: \(\d{2}\) \d{4,5}-\d{4}'
    match = re.search(pattern, content.replace('\n', ''))
    if match:
        return match.group().split(':')[1].strip()
    return None


def collect_fax(content):
    pattern = r'Fax:'
    match = re.search(pattern, content)
    if match:
        return content.split('Fax: ')[1].strip()
    return None


def collect_cep(content):
    pattern = r'\d{5}-\d{3}'
    match = re.search(pattern, content)
    if match:
        return match.group()
    return None


def collect_fip(content):
    pattern = r'\d{2,5}'
    match = re.search(pattern, content)
    if match:
        return match.group().strip()
    return None


def collect(url, data):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    driver.implicitly_wait(5)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'onetrust-banner-sdk')))
    WebDriverWait(driver, 60).until_not(EC.visibility_of_element_located((By.ID, 'onetrust-banner-sdk')))
    navibar = driver.find_element(By.CLASS_NAME, "wrap-aba")
    child_elements = navibar.find_elements(By.XPATH, "./*")
    navigation = {}
    for button in child_elements:
        letter = button.text
        navigation[letter] = button.get_attribute("class")

    print('#' * 50)
    print(f'Collecting letter: A')
    collect_table_data(driver, data)
    print()
    print()

    # letters = list(filter(lambda x: x != 'A', navigation.keys()))
    letters = list(filter(lambda x: x != 'A', navigation.keys()))
    for index in range(1, len(letters)):
        print('#' * 50)
        print(f'Collecting letter: {letters[index]}')
        try:
            driver.implicitly_wait(2)
            click_nav_btn(driver, index)
            driver.implicitly_wait(2)
            print()
            collect_table_data(driver, data)
            print()
        except Exception as e:
            print('>> error')
            print(e)
            print()
            continue
        finally:
            driver.implicitly_wait(2)
    # Close the browser
    driver.quit()


def collect_data(url, out_path, separator):
    if os.path.isfile(out_path):
        return pd.read_csv(out_path, sep=separator)
    else:
        data = {
            'name': [],
            'content': []
        }
        collect(url, data)
        df = pd.DataFrame(data)
        df.to_csv(out_path, sep=separator)
        return df
