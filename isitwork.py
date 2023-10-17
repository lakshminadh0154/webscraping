import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL of the Amazon search results page you want to scrape
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

# Create empty lists to store the data
product_urls = []
product_names = []
product_prices = []
ratings = []
review_counts = []


# connection as user
headers = {
        "User-Agent": "https://explore.whatismybrowser.com/useragents/parse/?analyse-my-user-agent=yes"
    }

# Define the number of pages to scrape (20 in your case)
num_pages = 20

# Loop through the pages and scrape data
for page in range(1, num_pages + 1):
    url = base_url + str(page)
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract product information
    products = soup.find_all('div', class_="sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 sg-col-12-of-24 s-list-col-right")

    for product in products:
        # Extract product URL
        product_link = product.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal', href=True)
        if product_link:
            product_urls.append("https://www.amazon.in" + product_link['href'])
        else:
            product_urls.append("N/A")

        # Extract product name
        product_name = product.find('span', class_='a-size-medium a-color-base a-text-normal')
        if product_name:
            product_names.append(product_name.text)
        else:
            product_names.append("N/A")

        # Extract product price
        product_price = product.find('span', class_='a-price-whole')
        if product_price:
            product_prices.append(product_price.text)
        else:
            product_prices.append("N/A")

        # Extract rating
        rating = product.find('span', class_='a-icon-alt')
        if rating:
            ratings.append(rating.text)
        else:
            ratings.append("N/A")

        # Extract number of reviews
        review_count = product.find('span', class_='a-size-base s-underline-text')
        if review_count:
            review_counts.append(review_count.text)
        else:
            review_counts.append("N/A")
        

# Create a Pandas DataFrame
data = {
    'Product URL': product_urls,
    'Product Name': product_names,
    'Product Price': product_prices,
    'Rating': ratings,
    'Number of Reviews': review_counts
    
}
df = pd.DataFrame(data)

# Save the data to a CSV file
df.to_csv('amazon_products.csv', index=False)
