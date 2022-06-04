from datetime import datetime
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option("useAutomationExtension", False)
service = ChromeService(executable_path="T:\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
import requests
import pandas

# variables
product_prices = []
product_titles = []
product_links = []
product_img_links = []
product_ratings = []
product_b_points = []
product_price_inrs = []
timestamp = []
product_sellers = []
bullets = []

def scrap_data():
    driver.get("https://www.amazon.de/s?me=A1J99ZSJJL0INS")
    while True:
        items = driver.find_elements(By.CLASS_NAME, "s-asin")
        for item in items:
            title_class = "a-size-medium.a-color-base.a-text-normal"
            title_link = item.find_element(By.CLASS_NAME, title_class)
            title = title_link.text
            product_titles.append(title)

            link_class ="a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal"
            p_link = item.find_element(By.CLASS_NAME, link_class)
            prod_link = p_link.get_attribute("href")
            product_links.append(prod_link)

            prices = item.find_element(By.CLASS_NAME, "a-price-whole").text
            product_prices.append(prices)
            
            # For Extra Credit: 1
            price_in_inr = requests.get(f"https://api.frankfurter.app/latest?amount={prices}&from=EUR&to=INR")
            product_price_inrs.append(price_in_inr.json()['rates']["INR"])

            image_link = item.find_element(By.CLASS_NAME, "s-image").get_attribute("src")
            product_img_links.append(image_link)

            ratings = item.find_element(By.CLASS_NAME, "a-icon-alt").get_attribute("innerHTML")
            product_ratings.append(ratings)

            timestamp.append(datetime.now())
        
        try:
            driver.get(driver.find_element(By.CLASS_NAME, "s-pagination-next").get_attribute("href"))
        except Exception as e:
            break

def product_info():
    driver.get("https://www.amazon.de/s?me=A1J99ZSJJL0INS")
    while True:
        
        for i in range(len(driver.find_elements(By.CLASS_NAME, "s-asin"))):
            items_new = driver.find_elements(By.CLASS_NAME, "s-asin")
            try:
                driver.get(items_new[i].find_element(By.CLASS_NAME, "a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal").get_attribute("href"))

            except Exception as e:
                if i < len(items_new):
                    driver.get(items_new[i+1].find_element(By.CLASS_NAME, "a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal").get_attribute("href"))
            
            seller = driver.find_element(By.ID, "merchant-info").find_element(By.TAG_NAME, "a").find_element(By.TAG_NAME, "span").get_attribute("innerHTML")
            product_sellers.append(seller)
                    
            driver.back()

        try:
            driver.get(driver.find_element(By.CLASS_NAME, "s-pagination-next").get_attribute("href"))
        except Exception as e:
            break

def main():
    print("Fetching product info ...")
    product_info()
    print("Scrapping data ...")
    scrap_data()
    driver.close()
    print("Writing data to file ...")
    df = pandas.DataFrame({"Title":product_titles,"Rating":product_ratings,"Price_in_EUR":product_prices,"Seller": product_sellers,"Price_in_INR":product_price_inrs,"Image":product_img_links,"Product_link":product_links,"Timestamp":timestamp})
    df.to_csv("amazon_data.csv", index=False, date_format='%Y-%m-%d %H:%M:%S')
    print("Finished.")
    
if __name__== "__main__":
    main()
