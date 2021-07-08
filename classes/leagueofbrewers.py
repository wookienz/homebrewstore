from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver
import time


class leagueofbrewers():
    """

    """

    def __init__(self):
        """

        :param self:
        :return:
        """
        self.BASE_URL = 'https://leagueofbrewers.co.nz/homebrew-beer-supplies/beer-brewing-ingredients/'
        self.grain_url = 'malt-for-making-beer/grain-for-brewing'
        self.yeast_url = 'beer-brewing-yeast'
        self.hops_url = 'hops-for-brewing-beer'
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
        for product in soup.findAll(class_='product-image'):
            product_name = product.img['alt']
            product_price = product.find(class_='price').text
            product_link = product.a['href']
            if product.find(class_='backorder'):
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
    t = leagueofbrewers()
    t.update_products()
