from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class AmazonCrawler:
    def __init__(self, user_query):
        self.query = user_query

    def sort_price(self, products):
        products.sort(key=lambda x: float(x['Price'].replace(',', '')) if x['Price'] != "No price available" else 0)
        return products

    def amazon_crawler(self):
        if self.query[1] != "":
            if self.query[1] == "new":
                amazon_link = f"https://www.amazon.co.uk/s?k={self.query[0]}&ref=nb_sb_noss_2&rh=p_n_condition-type%3A12319067031"
            elif self.query[1] == "used":
                amazon_link = f"https://www.amazon.co.uk/s?k={self.query[0]}&ref=nb_sb_noss_2&rh=p_n_condition-type%3A12319068031"
        else:
            amazon_link = f"https://www.amazon.co.uk/s?k={self.query[0]}&ref=nb_sb_noss_2"
        print(amazon_link)

        # Set up Selenium WebDriver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(amazon_link)

        # accept cookies
        try:
            driver.find_element(By.ID, 'sp-cc-accept').click()
        except:
            pass

        # Set up variables to store product data
        unique_products = set()
        products = []

        # Extract the total number of pages
        try:
            time.sleep(5)
            # Wait for the pagination elements to be present
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 's-pagination-item'))
            )

            # Find all elements with the class 's-pagination-item s-pagination-disabled'
            try:
                pagination_elements = driver.find_elements(By.CLASS_NAME, 's-pagination-item.s-pagination-disabled')
                total_pages = int(pagination_elements[-1].text)
            except:
                total_pages = 1


            # Extract and print the name and price of each product
            for page in range(1, total_pages + 1):
                if len(products) >= self.query[2]:
                    break

                driver.get(f"{amazon_link}&page={page}")

                # Wait for the product elements to be present
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 's-main-slot'))
                )

                # Find all product elements
                product_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'template=SEARCH')]")
                for product in product_elements[:self.query[2]]:
                    try:
                        name = product.find_element(By.CLASS_NAME, 'a-size-medium.a-color-base.a-text-normal').text
                    except:
                        name = "No name available"

                    try:
                        price_whole = product.find_element(By.CLASS_NAME, 'a-price-whole').text
                        price_fraction = product.find_element(By.CLASS_NAME, 'a-price-fraction').text
                        price = f"{price_whole}.{price_fraction}"
                    except:
                        price = "No price available"

                    try:
                        link = product.find_element(By.CLASS_NAME, 'a-link-normal.a-text-normal').get_attribute('href')
                    except:
                        link = "No link available"  

                    # Check if the product is unique
                    product_info = (name, price)
                    if product_info not in unique_products:
                        unique_products.add(product_info)
                        products.append(
                            {
                                'Title': name,
                                'Price': price,
                                'Condition': None,
                                'Link': link
                            }
                        )
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            driver.quit()

        return products

    def run(self):
        amazon_product_data = self.amazon_crawler()
        amazon_product_data = self.sort_price(amazon_product_data)
        return amazon_product_data