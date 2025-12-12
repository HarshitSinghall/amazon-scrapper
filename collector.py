from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os

def collect_data(keyword, max_pages, data_folder):
    """Collect product data from Amazon and save as HTML files"""
    
    # Create data folder if it doesn't exist
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    
    # Start Chrome browser
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)
    file = 1
    skipped_count = 0
    
    try:
        for i in range(1, max_pages + 1):
            url = f"https://www.amazon.in/s?k={keyword.replace(" ", "+")}&page={i}&crid=3GJ7S0QWWNCP0&qid=1765479616&sprefix=mobile%2Caps%2C508&xpid=1n4ZVr0HNNA3c&ref=sr_pg_2"
            driver.get(url)
            time.sleep(3)  # Wait for the page to load
            
            products_list = driver.find_elements(By.CLASS_NAME, "sg-col-inner")
            print(f"Page {i} has {len(products_list)} products.")
            
            for product in products_list:
                html_content = product.get_attribute('innerHTML').strip()
                if html_content != "":
                    
                    # Only save if there are enough lines
                    if len(html_content) > 2500:
                        with open(f"{data_folder}/{keyword}_{file}.html", "w", encoding="utf-8") as f:
                            f.write(html_content)
                        file += 1
                    else:
                        skipped_count += 1
        
        print(f"\nTotal files saved: {file - 1}")
        print(f"Total files skipped: {skipped_count}")
        
    finally:
        # Close the browser
        driver.quit()
    
    return file - 1  # Return number of files saved