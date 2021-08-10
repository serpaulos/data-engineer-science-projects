from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import time

options = Options()
options.add_argument("start-maximized")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Chrome('./chromedriver', options=options)

#get the actual data in order to use it as a placeholder to define folder/file name
actualdate = time.strftime("%d-%m-%Y")

categories = [
'travel', 'mystery', 'historical-fiction', 'sequential-art', 'classics', 'philosophy', 'romance', 'womens-fiction',
'fiction', 'childrens', 'religion', 'nonfiction', 'music', 'default', 'science-fiction', 'sports-and-games',
'add-a-comment', 'fantasy', 'new-adult', 'young-adult', 'science', 'poetry', 'paranormal', 'art', 'psychology',
'autobiography', 'parenting', 'adult-fiction', 'humor', 'horror', 'history', 'food-and-drink', 'christian-fiction',
'business', 'biography', 'thriller', 'contemporary', 'spirituality', 'academic', 'self-help', 'historical',
'christian', 'suspense', 'short-stories', 'novels', 'health', 'politics', 'cultural', 'erotica', 'crime'
]

#Defining columns to be loaded latter
df = pd.DataFrame(columns=["Category", "Title", "Price","Rating", "In stock"])
books = []

for (i, item) in enumerate(categories,2):
    driver.get(f"https://books.toscrape.com/catalogue/category/books/{item}_{i}/")
    webaddr = driver.current_url

    response = requests.get(webaddr)
    data = response.text
    soup = bs(data, "html.parser")
    contents = soup.select('ol li')

    for item in contents:
        category = driver.find_element_by_xpath('//div[@class="page-header action"]/h1').text
        title = item.find('h3').text
        price = item.find('p', class_='price_color').text
        price = price.replace('Â£', '')
        rating_class = item.find('p').attrs
        rating = rating_class['class'][1]
        stock = item.find('p', class_='instock availability').text.strip()

        books_info = {
            'Category': category,
            'Title': title,
            'Price': price,
            'Rating': rating,
            'Stock': stock
        }

        books.append(books_info)

time.sleep(2)
# Clean up (close browser once completed task).
driver.close()

df = pd.DataFrame(books)
df.to_csv('./data/books/'+actualdate+'-books.csv',header=False, index=False, encoding='utf-8')