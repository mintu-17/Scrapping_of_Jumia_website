pip install requests beautifulsoup4

from bs4 import BeautifulSoup
import requests

import pandas as pd
import numpy as np

url = "https://www.jumia.com.ng/category-fashion-by-jumia/"
response = requests.get(url)
response.content


import time

# Initialize lists to store product information
name_info = []
price_info = []
rating_info = []

# User-Agent header to mimic a web browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


# Number of pages to scrape
num_pages = 50
for page in range(1, num_pages + 1):
    url = f"https://www.jumia.com.ng/category-fashion-by-jumia/?page={page}#catalog-listing"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print(f"Successfully fetched the webpage for page {page}")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Locate the product details within the HTML
        product_containers = soup.find_all('article', class_='prd _fb col c-prd')
        
        for product in product_containers:
            name_tag = product.find('h3', class_='name')
            price_tag = product.find('div', class_='prc')
            rating_tag = product.find('div', class_='stars _s')
            
            # Extract and clean text only if the elements are found
            if name_tag and price_tag:
                name = name_tag.text.strip()
                price = price_tag.text.strip()
                rating = rating_tag.text.strip() if rating_tag else "No rating"
                
                name_info.append(name)
                price_info.append(price)
                rating_info.append(rating)
                
        # Adding a delay between requests to prevent being blocked
        time.sleep(1)
    else:
        print(f"Failed to fetch the webpage for page {page}", response.status_code)
        break



# Print the results (you can modify this part as needed)
print("Product Names:", name_info)
print("Product Prices:", price_info)
print("Product Ratings:", rating_info)


dict={'Product Name':name_info,'Price':price_info,'Rating':rating_info}

df=pd.DataFrame(dict)
df

df.to_csv('category_fashion_by_jumia.csv',index=False,encoding='utf-8')
