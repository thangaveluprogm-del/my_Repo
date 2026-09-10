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


df_books = pd.DataFrame(scraped_books)


display(df_books.head())
print(f"Total books scraped: {df_books.shape[0]}")

rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
df_books['rating'] = df_books['star_rating'].map(rating_map)

df_books['in_stock'] = df_books['availability'].apply(lambda x: 'In stock' in x)

display(df_books.head())
print(df_books.info())
# Define the fixed conversion rate
GBP_TO_INR_RATE = 105.50

# Convert price_gbp to price_inr
df_books['price_inr'] = df_books['price_gbp'] * GBP_TO_INR_RATE

# Display the DataFrame with the new 'price_inr' column
display(df_books.head())
print(df_books.info())

import sqlite3
conn = sqlite3.connect(':memory:')
c = conn.cursor()

# Create the categories table
c.execute('''
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL
)
''')
category_id_map = {}
first=c.execute('SELECT category_id, category_name FROM categories')
print(first.fetchall())
for row in c.fetchall():
    category_id_map[row[1]] = row[0]
books_to_insert = []
for index, row in df_books.iterrows():
    category_id = category_id_map.get(row['category'])
    # Convert boolean in_stock to integer (0 or 1) for SQLite
    in_stock_int = 1 if row['in_stock'] else 0
    books_to_insert.append((row['title'], row['price_gbp'], row['price_inr'],
                            row['rating'], in_stock_int, category_id))
print(books_to_insert)
second=c.executemany('INSERT INTO books (title, price_gbp, price_inr, rating, in_stock, category_id) VALUES (?, ?, ?, ?, ?, ?)', books_to_insert)
conn.commit()
print("Database schema created and data inserted successfully.")
# Verify data (optional)
print("\nCategories table content:")
for row in c.execute('SELECT * FROM categories').fetchall():
    print(row)
print("\nBooks table content (first 5 rows):")
for row in c.execute('SELECT * FROM books LIMIT 5').fetchall():
    print(row)
conn.close()


conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL
)
''')
unique_categories = df_books['category'].unique()
for category_name in unique_categories:
    c.execute('INSERT OR IGNORE INTO categories (category_name) VALUES (?)', (category_name,))
c.execute('''
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price_gbp REAL,
    price_inr REAL,
    rating INTEGER,
    in_stock INTEGER,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
)
''')
category_id_map = {}
c.execute('SELECT category_id, category_name FROM categories')
for row in c.fetchall():
    category_id_map[row[1]] = row[0]
books_to_insert = []
for index, row in df_books.iterrows():
    category_id = category_id_map.get(row['category'])
    in_stock_int = 1 if row['in_stock'] else 0
    books_to_insert.append((row['title'], row['price_gbp'], row['price_inr'],
                            row['rating'], in_stock_int, category_id))
c.executemany('INSERT INTO books (title, price_gbp, price_inr, rating, in_stock, category_id) VALUES (?, ?, ?, ?, ?, ?)', books_to_insert)

conn.commit()
print("Database re-created and data re-inserted successfully for querying.")


query1 = "SELECT title, rating FROM books WHERE rating = 5"
c.execute(query1)
print(f"Query: {query1}")
for row in c.fetchall():
    print(row)

query2 = "SELECT title, price_gbp FROM books ORDER BY price_gbp DESC LIMIT 5"
c.execute(query2)
print(f"Query: {query2}")
for row in c.fetchall():
    print(row)

query3 = "SELECT DISTINCT category_name FROM categories ORDER BY category_name"
c.execute(query3)
print(f"Query: {query3}")
for row in c.fetchall():
    print(row)

query4 = "SELECT title, price_gbp FROM books WHERE price_gbp BETWEEN 20 AND 30 ORDER BY price_gbp"
c.execute(query4)
print(f"Query: {query4}")
for row in c.fetchall():
    print(row)

query5 = """
SELECT b.title, c.category_name, b.rating
FROM books b
JOIN categories c ON b.category_id = c.category_id
ORDER BY c.category_name, b.rating DESC
LIMIT 10
"""
c.execute(query5)
print(f"Query: {query5}")
for row in c.fetchall():
    print(row)


conn.close()
print("\nDatabase connection closed.")

# --- 1. Read two query results into pandas DataFrames using pd.read_sql ---

print("\n--- Query 1: Books with a 5-star rating (using pd.read_sql) ---")
query_five_star_books = "SELECT title, rating FROM books WHERE rating = 5 ORDER BY title LIMIT 10"
df_five_star = pd.read_sql(query_five_star_books, conn)
display(df_five_star)

print("\n--- Query 2: Top 5 Most Expensive Books in INR (using pd.read_sql) ---")
query_top_expensive_inr = "SELECT title, price_inr FROM books ORDER BY price_inr DESC LIMIT 5"
df_top_inr = pd.read_sql(query_top_expensive_inr, conn)
display(df_top_inr)
print("\n--- Query 2: Top 5 Most Expensive Books in INR (using pd.read_sql) ---")
query_top_expensive_inr = "SELECT title, price_inr FROM books ORDER BY price_inr DESC LIMIT 5"
df_top_inr = pd.read_sql(query_top_expensive_inr, conn)
display(df_top_inr)
