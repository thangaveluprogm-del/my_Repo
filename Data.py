import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

BASE_URL = 'http://books.toscrape.com/'

def scrape_books_data(num_pages=5):
    books_data = []
    for page in range(1, num_pages + 1):
        print(f"Scraping page {page}...")
        url = f'{BASE_URL}catalogue/page-{page}.html'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        articles = soup.find_all('article', class_='product_pod')
        for article in articles:
            book_url_suffix = article.h3.a['href']
           
            if 'catalogue' not in book_url_suffix:
                book_url = f'{BASE_URL}catalogue/{book_url_suffix}'
            else:
                book_url = f'{BASE_URL}{book_url_suffix}'

           
            book_response = requests.get(book_url)
            book_soup = BeautifulSoup(book_response.content, 'html.parser')

            title = book_soup.find('h1').text
            price_text = book_soup.find('p', class_='price_color').text
            print(f"Original price_text: '{price_text}'") 
            price = re.sub(r'[^0-9.]', '', price_text) 
            print(f"Cleaned price: '{price}'") 
            star_rating_text = book_soup.find('p', class_='star-rating')['class'][1] 
            availability = book_soup.find('p', class_='availability').text.strip()

           
            breadcrumbs = book_soup.find('ul', class_='breadcrumb').find_all('li')
            category = breadcrumbs[2].a.text 

            books_data.append({
                'title': title,
                'price_gbp': float(price),
                'star_rating': star_rating_text,
                'availability': availability,
                'category': category
            })
            time.sleep(0.1) # Be polite, add a small delay
    return books_data

scraped_books = scrape_books_data(num_pages=5)

# Convert to DataFrame
df_books = pd.DataFrame(scraped_books)

# Display the first few rows and the shape of the DataFrame
display(df_books.head())
print(f"Total books scraped: {df_books.shape[0]}")
