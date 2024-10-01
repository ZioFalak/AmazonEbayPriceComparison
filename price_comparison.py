import amazon_crawler
import ebay_crawler
import csv

class PriceComparison:
    def __init__(self):
        self.query = self.get_query()
        self.amazon_crawler = amazon_crawler.AmazonCrawler(self.query)
        self.ebay_crawler = ebay_crawler.EbayCrawler(self.query)

    def blank_input(self, input):
        return input.strip() == ""

    def get_query(self):
        product_input = input("Enter the product you want to search: ")
        while self.blank_input(product_input):
            product_input = input("Please enter a valid product: ")
        product_input = product_input.replace(" ", "+")

        product_condition = input("Enter condition (new / used or leave blank for both): ")
        while product_condition != "new" and product_condition != "used" and product_condition != "":
            product_condition = input("Please enter a valid condition: ")

        num_to_display = input("Enter the number of products to display: (Default: 10) ")
        if self.blank_input(num_to_display):
            num_to_display = 10
        else:
            while not num_to_display.isdigit():
                num_to_display = input("Please enter a valid number: ")
            num_to_display = int(num_to_display)

        return product_input, product_condition, int(num_to_display)

    def write_to_csv(self, products):
        # Sort products by Price
        sorted_products = sorted(products, key=lambda x: float(x['Price'].replace('£', '').replace(',', '')) if x['Price'] != "No price available" else 0)

        file = 'products.csv'
        with open(file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Price', 'Condition', 'Link'])
            for product in sorted_products:
                writer.writerow([product['Title'], product['Price'], product['Condition'], product['Link']])

    def first_three_products(self, products, name):
        try:
            print(f"\nTop 3 {name} products:")
            for product in products[:3]:
                for key, value in product.items():
                    print(f"{key}: {value}")
        except:
            print("No products found")

    def run(self):
        amazon_product_data = self.amazon_crawler.run()
        ebay_product_data = self.ebay_crawler.run()

        self.first_three_products(amazon_product_data, "Amazon")
        self.first_three_products(ebay_product_data, "eBay")
            
        # Combine Amazon and eBay product data
        combined_products = amazon_product_data + ebay_product_data
        
        # Write combined and sorted products to CSV
        try:
            self.write_to_csv(combined_products)
            print("\nProducts written to products.csv")
        except:
            print("No products found. Nothing written to CSV")


    
price_comparison = PriceComparison()
price_comparison.run()