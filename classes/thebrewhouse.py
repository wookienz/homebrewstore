from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver
import time


class thebrewhouse():
    """

    """

    def __init__(self):
        """

        :param self:
        :return:
        """
        self.BASE_URL = 'https://www.thebrewhouse.co.nz/beer/'
        self.grain_url = '3'
        self.yeast_url = '8'
        self.hops_url = '11'
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
        NOT REQUIRED FOR THIS SITE
        :return:
        """
        html = self._parseurl(url)
        return html.text

    def _parseurl(self, url, sub='get', payload=''):
        if sub == 'get':
            r = self.s.get(url, verify=False)
        else:
            r = self.s.post(url, data=payload, verify=False)
        return r

    def _update_single_product(self, html):
        """
        works for malt, yeast and hops. doest load the whole page however, need to work out how to JS loading whole page

        :param html: html from site for that product
        :return:
        """
        product_details = []
        soup = BeautifulSoup(html, features="html.parser")
        products = soup.find('div', {'class': 'brewhouse-listing'}).findAll('li')
        for product in products:
            product_name = product.h3.text
            product_price = product.p.span.text
            product_link = product.a['href']
            if product_price == 'OUT OF STOCK':
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
    t = thebrewhouse()
    t.update_products()