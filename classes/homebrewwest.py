from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver
import time

# malts https://www.homebrewwest.co.nz/products/category/21/malts-grain?pgNmbr=4&pgSize=25&isScrollChunk=true&chunkNumber=4
#yeast https://www.homebrewwest.co.nz/products/category/34/beer-yeast?pgNmbr=4&pgSize=25&isScrollChunk=true&chunkNumber=4
#hops https://www.homebrewwest.co.nz/products/category/20/hops?pgNmbr=3&pgSize=25&isScrollChunk=true&chunkNumber=4
#make class, load urls in here, make functions for updating etc.
class homebrewwest():
    """

    """
    def __init__(self):
        """

        :param self:
        :return:
        """
        self.BASE_URL = 'https://www.homebrewwest.co.nz/products/category/'
        self.grain_url = '21/malts-grain?pgNmbr=4&pgSize=25&isScrollChunk=true&chunkNumber=4'
        self.yeast_url = '34/beer-yeast?pgNmbr=4&pgSize=25&isScrollChunk=true&chunkNumber=4'
        self.hops_url = '20/hops?pgNmbr=3&pgSize=25&isScrollChunk=true&chunkNumber=4'
        self.all_urls = [self.hops_url, self.grain_url, self.yeast_url]
        self.s = requests.session()
        return

    def update_products(self):
        """
        go through all types of products and update the database
        :return:
        """
        for product_url in self.all_urls:
            entire_page = self._load_entire_page(self.BASE_URL+product_url)
            details = self._update_single_product(entire_page)
            self._store(details)
        return

    def _load_entire_page(self, url):
        """
        Use selenium driver to load chrome, scroll then pass resultant html.
        :return:
        """
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('chromedriver')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        ScrollNumber = 20
        for i in range(1, ScrollNumber):
            driver.execute_script("window.scrollTo(1,50000)")
            time.sleep(1)
        return driver.page_source

    def _parseurl(self, url, sub='get', payload=''):
        if sub == 'get':
            r = self.s.get(url, verify=False)
        else:
            r = self.s.post(url, data=payload, verify=False)
        return r

    def _update_single_product(self, html):
        """
        works for malt, yeast and hops. doest load the whole page however, need to work out how to JS loading whole page

        :param product_url: 'beer-brewing-yeast'
        :return:
        """
        product_details = []
        soup = BeautifulSoup(html, features="html.parser")
        for product in soup.findAll(class_='product'):
            product_name = (product.find(class_='name').text).strip()
            product_price = (product.find(class_='price').text).strip()
            product_link = product.a['href']
            if product.find(class_='backorder'): #check works.
                product_availability = 0
            else:
                product_availability = 1
            product_details.append((product_name, product_price, product_link, product_availability))
        return product_details

    def _store(self, deets_array):
        """
        Store the details of the items
        :return:
        """
        for a in deets_array:
            for b in a:
                print(b)


if __name__ == '__main__':
    t = homebrewwest()
    t.update_products()
