from selenium.webdriver.common.by import By


def collect_table_data(driver, df):
    accordions = driver.find_elements(By.CLASS_NAME, 'wrap-content')
    print(len(accordions))
    for accordion in accordions:
        print('-' * 40)
        try:
            accordion.click()
            driver.implicitly_wait(3)
            title = accordion.find_element(By.CLASS_NAME, 'accordion-title-content')
            name = title.text
            print(name)
            description = accordion.find_element(By.CLASS_NAME, 'accordion-description')
            # description = accordion.find_element(By.XPATH, '/main/div/p')
            p_tag = description.find_element(By.TAG_NAME, 'p')
            s_description = p_tag.text
            print(s_description)
            df['name'].append(name)
            df['content'].append(s_description)
        except Exception:
            print('Erro')
            continue
        finally:
            driver.implicitly_wait(1)


def click_nav_btn(driver, child_index):
    button = driver.find_element(By.CSS_SELECTOR, "div.wrap-aba button:nth-child({})".format(child_index))
    # buttons = driver.find_element(By.CLASS_NAME, "wrap-aba")
    # button = buttons.find_element(By.XPATH, "//button[contains(., '{}')]".format(letter))
    button.click()


