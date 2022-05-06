from selenium import webdriver
import requests
import pandas
from datetime import datetime

# variables
products_price = []
products_title = []
products_link = []
products_img_link = []
products_rating = []
products_b_point = []
products_price_inr = []
timestamp = []
driver = webdriver.Chrome()


for page in range(1,3):
    driver.get("https://www.amazon.de/s?me=A1J99ZSJJL0INS&page={}".format(page))
    items = driver.find_elements_by_class_name("s-asin")
    for item in items:
        ratings = item.find_element_by_css_selector("div div.a-row.a-size-small").find_element_by_tag_name("span").get_attribute("aria-label")
        products_rating.append(ratings)

        price = item.find_element_by_class_name("a-price-whole")
        products_price.append(price.text)

        price_in_inr = requests.get("https://api.frankfurter.app/latest?amount={}&from=EUR&to=INR".format(price.text))
        products_price_inr.append(price_in_inr.json()['rates']["INR"])

        title = item.find_element_by_css_selector(".s-title-instructions-style a").text
        products_title.append(title)

        link = item.find_element_by_css_selector(".s-title-instructions-style a").get_attribute("href")
        products_link.append(link)

        image_link = item.find_element_by_class_name("s-image").get_attribute("src")
        products_img_link.append(image_link)

        timestamp.append(datetime.now())

df = pandas.DataFrame({"Title":products_title,"Rating":products_rating,"Price_in_EUR":products_price,"Price_in_INR":products_price_inr,"Image":products_img_link,"Product_link":products_link,"Timestamp":timestamp})
df.to_csv("amazon_data.csv", index=False, date_format='%Y-%m-%d %H:%M:%S')

driver.close()