import time 
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By 

BASE_URL = "https://www.baseball-almanac.com/yearmenu.shtml"
DATA_SAVE_PATH = "../data/events.csv"

# Configure Selenium
def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    driver = webdriver.Chrome(options=options)
    return driver 

# Scrape one page 
def scrape_page(driver):
    rows = driver.find_elements(By.CSS_SELECTOR, "table tr")
    data = []

    for row in rows[1:]:
        cols = row.find_elements(By.TAG_NAME, "td")
        try:
            year = cols[0].text.strip()
            event_name = cols[1].text.strip()
            description = cols[2].text.strip()
            data.append({
                "Year": year,
                "Event": event_name,
                "Description": description
            })
        except IndexError:
            continue 
    return data 

# Handle pagination 
def scrape_all_pages():
    driver = get_driver()
    driver.get(BASE_URL)
    all_data = []

    while True:
        time.sleep(1)
        page_data = scrape_page(driver)
        all_data.extend(page_data)

        try:
            next_button = driver.find_element(By.LINK_TEXT, "Next")
            if "disabled" in next_button.get_attribute("class"):
                break 
            next_button.click()
        except:
            break 

    driver.quit()
    return all_data 

if __name__=="__main__":
    print("Scraping data")
    results = scrape_all_pages()
    df = pd.DataFrame(results)
    df.to_csv(DATA_SAVE_PATH, index=False)
    print(f"Saved {len(df)} records to {DATA_SAVE_PATH}")

