from bs4 import BeautifulSoup
import requests
import re

class EbayCrawler:
    def __init__(self, user_query):
        self.query = user_query
    
    # Get price of product
    def product_price(self, price_string):
        substring = " to "
        if substring in price_string:
            price_string = price_string.split(substring)[0]

        # Remove all characters except digits and decimal point
        price = re.sub(r'[^\d.]', '', price_string)
        return float(price)

    # Sort products by price
    def sort_price(self, products):
        products.sort(key=lambda x: self.product_price(x['Price']))
        return products

    # Get product details from eBay
    def ebay_crawler(self):
        if self.query[1] != "":
            ebay_link = f"https://www.ebay.co.uk/sch/i.html?_nkw={self.query[0]}&_sacat=0&LH_BIN=1&_ipg=240&LH_ItemCondition={self.query[1]}"
        else:
            ebay_link = f"https://www.ebay.co.uk/sch/i.html?_nkw={self.query[0]}&_sacat=0&LH_BIN=1&_ipg=240"
        print(ebay_link)
        page = requests.get(ebay_link).text
        doc = BeautifulSoup(page, 'html.parser')

        # Get total pages
        try:
            page_tag = doc.find_all('ol', class_='pagination__items')
            pages = page_tag[0].find_all(recursive=False)
            total_pages = int(pages[-1].text)
        except:
            total_pages = 1

        # Get products from all pages
        products = []
        for i in range(1, total_pages + 1):
            if len(products) >= self.query[2]:
                break
            
            page = requests.get(f"{ebay_link}&_pgn={i}").text
            doc = BeautifulSoup(page, 'html.parser')

            # Get product card
            product_list = doc.find_all('li', {'class': 's-item', 'id': re.compile('item')})
            # Get product details
            for product in product_list[:self.query[2]]:
                title = product.find('span', role='heading').text
                price = product.find('span', class_='s-item__price').text
                condition = product.find('span', class_='SECONDARY_INFO').text
                link = product.find('a', class_='s-item__link').get('href')
                products.append({
                    'Title': title,
                    'Price': price,
                    'Condition': condition,
                    'Link': link
                })

        # Return dictionary of products
        return products

    # Prints all products on eBay
    def run(self):
        ebay_product_data = self.ebay_crawler()
        ebay_product_data = self.sort_price(ebay_product_data)
        return ebay_product_data