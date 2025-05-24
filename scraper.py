import requests
from bs4 import BeautifulSoup
import csv
import re

URL = 'https://www.amazon.com/s?k=smartphones&rh=n%3A21514055011%2Cp_n_deal_type%3A23566065011&dc&page=13&crid=2S726TJ1777CB&qid=1745269903&rnid=23566063011&sprefix=%2Caps%2C256&xpid=bzKDcqUW7UeLR&ref=sr_pg_13'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept-Language': 'en-US, en;q=0.5'
}

page = requests.get(URL, headers=HEADERS)
src = page.content
soup = BeautifulSoup(src, 'lxml')

products = soup.find('div', {'class': 's-main-slot s-result-list s-search-results sg-row'})
items = products.find_all('div', {'class': 'sg-col-inner'})

product_info = []
for i in items:
    product_name = model = product_price1 = product_price2 = product_delivery = product_bought1 = Discount_Percentage = None
    try:
        title = i.find('h2', class_='a-size-medium a-spacing-none a-color-base a-text-normal')
        if title:
            product_name = title.find('span').text.strip()
            model = product_name.split()[0]
        
        price1 = i.find('span', {'class': 'a-price a-text-price'})
        if price1:
            product_price1 = price1.find('span', {'class': 'a-offscreen'}).text.strip()

        price2 = i.find('span', {'class': 'a-price'})
        if price2:
            product_price2 = price2.find('span', {'class': 'a-offscreen'}).text.strip()

        if product_price1 and product_price2:
            prc1 = float(product_price1.replace('$', '').replace(',', '').strip())
            prc2 = float(product_price2.replace('$', '').replace(',', '').strip())
            Discount_Percentage = ((prc1 - prc2) / prc1) * 100

        delivery = i.find('div', {'class': 'a-row a-size-base a-color-secondary s-align-children-center'})
        if delivery:
            product_delivery = delivery.find('span', {'class': 'a-color-base a-text-bold'}).text.strip()

        bought_N = i.find('div', {'class': 'a-row a-size-base'})
        if bought_N:
            product_bought = bought_N.find('span', {'class': 'a-size-base a-color-secondary'})
            if product_bought:
                product_bought1 = product_bought.text.strip().split()[0]
        else:
            product_bought1 = None

        product_info.append({
            'Model': model,
            'Phone Details': product_name,
            'Original price': product_price1,
            'Discounted price': product_price2,
            'Discount Percentage': f"{Discount_Percentage:.2f}" if Discount_Percentage is not None else None,
            'Bought in past month': product_bought1,
            'Delivery Time': product_delivery
        })
    except Exception as e:
        print(f"Error processing a product: {e}")

keys = product_info[0].keys()
with open(r'C:\Users\Admin\OneDrive\Documents\Web_Scraping\Sheet_test.csv', 'a', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    # dict_writer.writeheader()
    dict_writer.writerows(product_info)
    print('Data written to CSV successfully!')



